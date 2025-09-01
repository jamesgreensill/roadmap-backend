import enum


class EventType(enum.Enum):
    CommitCommentEvent = enum.auto()
    CreateEvent = enum.auto()
    DeleteEvent = enum.auto()
    ForkEvent = enum.auto()
    GollumEvent = enum.auto()
    IssueCommentEvent = enum.auto()
    IssuesEvent = enum.auto()
    MemberEvent = enum.auto()
    PublicEvent = enum.auto()
    PullRequestEvent = enum.auto()
    PullRequestReviewEvent = enum.auto()
    PullRequestReviewCommentEvent = enum.auto()
    PullRequestReviewThreadEvent = enum.auto()
    PushEvent = enum.auto()
    ReleaseEvent = enum.auto()
    SponsorshipEvent = enum.auto()
    WatchEvent = enum.auto()


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
