from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from .models import Feed, Entry, Subscription, ReadStatus
import feedparser
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

@login_required
def feed_list(request):
    subscriptions = Subscription.objects.filter(user=request.user, is_active=True)
    return render(request, 'rss_reader/feed_list.html', {'subscriptions': subscriptions})

@login_required
def add_feed(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        feed = feedparser.parse(url)
        
        if not feed.bozo:  # フィードが有効な場合
            with transaction.atomic():
                feed_obj, created = Feed.objects.get_or_create(
                    url=url,
                    defaults={
                        'title': feed.feed.get('title', 'Untitled'),
                        'description': feed.feed.get('description', '')
                    }
                )
                Subscription.objects.get_or_create(user=request.user, feed=feed_obj)
            messages.success(request, 'Feed added successfully.')
            return redirect('rss_reader:update_feed', feed_id=feed_obj.id)
        else:
            messages.error(request, 'Invalid feed URL.')
        
        return redirect('rss_reader:feed_list')
    
    return render(request, 'rss_reader/add_feed.html')

@login_required
def feed_entries(request, feed_id):
    feed = get_object_or_404(Feed, id=feed_id)
    entries = Entry.objects.filter(feed=feed).order_by('-published_date')
    
    for entry in entries:
        entry.is_read = ReadStatus.objects.filter(user=request.user, entry=entry, is_read=True).exists()
    
    return render(request, 'rss_reader/feed_entries.html', {'feed': feed, 'entries': entries})

@login_required
def mark_as_read(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    ReadStatus.objects.get_or_create(user=request.user, entry=entry, defaults={'is_read': True})
    return redirect('rss_reader:feed_entries', feed_id=entry.feed.id)

@login_required
def update_feed(request, feed_id):
    feed = get_object_or_404(Feed, id=feed_id)
    
    try:
        with transaction.atomic():
            parsed_feed = feedparser.parse(feed.url)
            
            for entry in parsed_feed.entries:
                published = entry.get('published_parsed') or entry.get('updated_parsed')
                if published:
                    published_date = datetime.fromtimestamp(time.mktime(published))
                    published_date = timezone.make_aware(published_date)
                else:
                    published_date = timezone.now()
                
                entry_obj, created = Entry.objects.get_or_create(
                    feed=feed,
                    link=entry.link,
                    defaults={
                        'title': entry.title,
                        'description': entry.get('description', ''),
                        'published_date': published_date,
                        'author': entry.get('author', '')
                    }
                )
                
                if created:
                    logger.info(f"New entry created: {entry_obj.title}")
                
            feed.last_updated = timezone.now()
            feed.save()
        
        messages.success(request, f'Feed "{feed.title}" updated successfully.')
    except Exception as e:
        logger.error(f"Error updating feed {feed.id}: {str(e)}")
        messages.error(request, f'Error updating feed: {str(e)}')
    
    return redirect('rss_reader:feed_entries', feed_id=feed.id)

@login_required
def update_all_feeds(request):
    subscriptions = Subscription.objects.filter(user=request.user, is_active=True)
    
    for subscription in subscriptions:
        update_feed(request, subscription.feed.id)
    
    return redirect('rss_reader:feed_list')