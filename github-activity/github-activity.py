import argparse
import requests
import enum
import os
import json

# https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28


class ApiLoader:
    @staticmethod
    def load(filepath: str):
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None, None

        hostname = data.get('hostname')
        endpoints = data.get('endpoints')

        if not hostname or not isinstance(endpoints, dict):
            return None, None

        return hostname, endpoints


class ApiBuilder:
    @staticmethod
    def build_api(hostname: str, endpoints: dict):
        api = type('API', (), {})()
        for name, path in endpoints.items():
            setattr(api, name, f"{hostname}{path}")
        return api    


class ApiObject:
    def __init__(self, id: int):
        self.id = id
        pass


class Actor(ApiObject):
    def __init__(self, id: int, login: str, display_login: str, url: str):
        self.login = login
        self.display_login = display_login
        self.url = url
        super().__init__(id)
        pass

    # expects dictionary to be structured:
    # data = {
    #   "id" : "<value>",
    #   "login" : "<value>",
    #   "display_login"  : "<value>",
    #   "url" : "<value>"
    # }
    @staticmethod
    def from_data(data: dict):
        id = int(data.get('id'))
        login = data.get('login')
        display_login = data.get('display_login')
        url = data.get('url')

        assert id is not None
        assert login is not None
        assert display_login is not None
        assert url is not None

        return Actor(id, login, display_login, url)


class Repository(ApiObject):
    def __init__(self, id: int, name: str, url: str):
        self.name = name
        self.url = url

        super().__init__(id)
        pass

    # expects dictionary to be structured:
    # data = {
    #   "id" : "<value>",
    #   "name" : "<value>",
    #   "url"  : "<value>"
    # }

    @staticmethod
    def from_data(data: dict):
        id = int(data.get('id'))
        name = data.get('name')
        url = data.get('url')

        assert id is not None
        assert name is not None
        assert url is not None

        return Repository(id, name, url)

# This is the best way, I can think of having custom display messages,
# without having 4 large data structures or loading externally

# It can be formatted by:
# EventType.Event.value.format(actor=actor.login, repo=repo.name, count=count, plural="s" if count > 1 else ""))


class EventType(enum.Enum):
    CommitCommentEvent = "{actor} made {count} commit comment{plural} in {repo}"
    CreateEvent = "{actor} created {count} item{plural} in {repo}"
    DeleteEvent = "{actor} deleted {count} item{plural} from {repo}"
    ForkEvent = "{actor} forked {count} repository(ies) from {repo}"
    GollumEvent = "{actor} updated {count} wiki page{plural} in {repo}"
    IssueCommentEvent = "{actor} commented on {count} issue{plural} in {repo}"
    IssuesEvent = "{actor} opened {count} issue{plural} in {repo}"
    MemberEvent = "{actor} made {count} member change{plural} in {repo}"
    PublicEvent = "{actor} made {count} repository(ies) public in {repo}"
    PullRequestEvent = "{actor} opened {count} pull request{plural} in {repo}"
    PullRequestReviewEvent = "{actor} reviewed {count} pull request{plural} in {repo}"
    PullRequestReviewCommentEvent = "{actor} commented on {count} pull request review{plural} in {repo}"
    PullRequestReviewThreadEvent = "{actor} updated {count} pull request review thread{plural} in {repo}"
    PushEvent = "{actor} pushed {count} commit{plural} to {repo}"
    ReleaseEvent = "{actor} published {count} release{plural} in {repo}"
    SponsorshipEvent = "{actor} sponsored {count} repository(ies)} in {repo}"
    WatchEvent = "{actor} started watching {count} repository(ies) in {repo}"

    def build(self, actor, repo, count):
        return self.value.format(actor=actor, repo=repo, count=count, plural="s" if count > 1 else "")


class GitHubEvent(ApiObject):
    def __init__(self, id: int, type: EventType, actor: Actor, repository: Repository, created_at: str):
        self.id = id
        self.type = type
        self.actor = actor
        self.repository = repository
        self.created_at = created_at

        super().__init__(id)

    # expects dictionary to be structured:
    # data = {
    #   "id" : "<value>",
    #   "type" : "<value>",
    #   "actor"  : "{ ... }",
    #   "repo : "{ ... }"
    #   "created_at"  : "<value>",
    # }
    @staticmethod
    def from_data(data):
        id = int(data.get('id'))
        type = data.get('type')
        actor_data = data.get('actor')
        repository_data = data.get('repo')
        created_at = data.get('created_at')

        assert id is not None
        assert type is not None
        assert actor_data is not None
        assert repository_data is not None
        assert created_at is not None

        actor = Actor.from_data(actor_data)
        repository = Repository.from_data(repository_data)

        return GitHubEvent(id, EventType[type], actor, repository, created_at)


class EventSummarizer:
    def __init__(self, events):
        self.events = events
        pass

    def summarize(self):
        current_event = None
        count = 0
        for event in self.events:
            if count > 0 and (current_event.type != event.type or current_event.repository.id != event.repository.id):
                # We have encountered a new event type, display summary of previous event type
                print(current_event.type.build(current_event.actor.login,
                      current_event.repository.name, count))
                count = 0

            count += 1
            current_event = event
        pass


def main():
    hostname, endpoints = ApiLoader.load('api.json')
    api = ApiBuilder.build_api(hostname, endpoints)

    parser = argparse.ArgumentParser(
        prog='github-activity',
        description='A simple command line interface (CLI) to fetch the recent activity of a GitHub user'
    )

    parser.add_argument('username')
    arguments = parser.parse_args()

    assert arguments.username is not None

    request_uri = api.user_events.format(username=arguments.username)
    response = requests.get(request_uri)
    
    if not response.ok:
        print(f'Request failed: {request_uri} - {response.status_code} {response.reason}')
        return

    json = response.json()

    try:
        events = [GitHubEvent.from_data(event) for event in json]
    except AssertionError as error:
        print(f'Failed to parse response: {json}')
        return

    summarizer = EventSummarizer(events)
    summarizer.summarize()
    
main()
