import argparse
import requests
import ghapi
import apiloader
import re


class EventMessageBuilder:
    _EVENT_MESSAGES = {
        ghapi.EventType.CommitCommentEvent: ("made", "commit(s)"),
        ghapi.EventType.CreateEvent: ("created", "item(s)"),
        ghapi.EventType.DeleteEvent: ("deleted", "item(s)"),
        ghapi.EventType.ForkEvent: ("forked", "repositor[y](ies)"),
        ghapi.EventType.GollumEvent: ("updated", "wiki page(s)"),
        ghapi.EventType.IssueCommentEvent: ("commented on", "issue(s)"),
        ghapi.EventType.IssuesEvent: ("opened", "issue(s)"),
        ghapi.EventType.MemberEvent: ("made", "member change(s)"),
        ghapi.EventType.PublicEvent: ("made", "repositor[y](ies) public"),
        ghapi.EventType.PullRequestEvent: ("opened", "pull request(s)"),
        ghapi.EventType.PullRequestReviewEvent: ("reviewed", "pull request(s)"),
        ghapi.EventType.PullRequestReviewCommentEvent: ("commented on", "pull request review(s)"),
        ghapi.EventType.PullRequestReviewThreadEvent: ("updated", "pull request review thread(s)"),
        ghapi.EventType.PushEvent: ("pushed", "commit(s)"),
        ghapi.EventType.ReleaseEvent: ("published", "release(s)"),
        ghapi.EventType.SponsorshipEvent: ("sponsored", "repositor[y](ies)"),
        ghapi.EventType.WatchEvent: ("started watching", "repositor[y](ies)"),
    }

   # This will format the noun which contains both non-plural and plural definitons.
   # i;e repositor[y](ies)
   # Or cases, where the plural is appended to the word, rather than replaced.
   # i;e commit(s)
   # [text] = non-plural
   # (text) = plural
    @staticmethod
    def _collapase_schrodinger_noun(noun: str, count: int):
        noun = re.sub(
            r'\[([^\]]+)\]\(([^\)]+)\)',
            lambda m: m.group(2) if count > 1 else m.group(1),
            noun
        )
        noun = re.sub(
            r'([a-zA-Z]+)\(([^)]+)\)',
            lambda m: m.group(1) + m.group(2) if count > 1 else m.group(1),
            noun
        )
        return noun

    @classmethod
    def build(cls, event: ghapi.GitHubEvent, count: int):
        event_type = event.type
        repository = event.repository
        actor = event.actor

        if event_type not in cls._EVENT_MESSAGES:
            return f'{actor.login} did something in {repository.name}'

        verb, noun = cls._EVENT_MESSAGES[event_type]
        collapsed_noun = cls._collapase_schrodinger_noun(noun, count)

        return f'{actor.login} {verb} {count} {collapsed_noun} in {repository.name}'


class EventSummary:
    def __init__(self, event, count):
        self.event = event
        self.count = count


class EventSummarizer:
    def __init__(self, events):
        self.events = events
        pass

    def summarize(self):
        summarized_events = []
        current_event = None
        count = 0
        for event in self.events:
            if count > 0 and (current_event.type != event.type or current_event.repository.id != event.repository.id):
                # We have encountered a new event type, display summary of previous event type
                summarized_events.append(EventSummary(current_event, count))
                count = 0

            count += 1
            current_event = event
        return summarized_events


def main():
    parser = argparse.ArgumentParser(
        prog='github-activity',
        description='A simple command line interface (CLI) to fetch the recent activity of a GitHub user'
    )
    parser.add_argument('username')
    arguments = parser.parse_args()

    api = apiloader.Builder.build_api(*apiloader.Loader.load('api.json'))

    headers = {'User-Agent': "Github-Activity/1.0"}
    request_uri = api.user_events.format(
        username=arguments.username)
    response = requests.get(request_uri, headers=headers)

    if not response.ok:
        print(
            f'Request failed: {request_uri} - {response.status_code} {response.reason}')
        return

    events_data = response.json()

    try:
        events = [ghapi.GitHubEvent.from_data(event) for event in events_data]
    except AssertionError as error:
        print(f'Failed to parse response: {events_data}')
        return

    summarizer = EventSummarizer(events)
    summarized_events = summarizer.summarize()

    for summary in summarized_events:
        event_message = EventMessageBuilder.build(summary.event, summary.count)
        print(event_message)


main()
