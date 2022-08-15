# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = Statusfromdict(json.loads(json_string))

from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from enum import Enum
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Detail:
    type: str
    text: Optional[str]

    def __init__(self, type: str, text: Optional[str]) -> None:
        self.type = type
        self.text = text

    @staticmethod
    def from_dict(obj: Any) -> 'Detail':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        text = from_union([from_str, from_none], obj.get("text"))
        return Detail(type, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["text"] = from_union([from_str, from_none], self.text)
        return result


class Covers:
    cover: str
    cover2x: str
    card: str
    card2x: str
    list: str
    list2x: str
    slimcover: str
    slimcover2x: str

    def __init__(self, cover: str, cover2x: str, card: str, card2x: str, list: str, list2x: str, slimcover: str, slimcover2x: str) -> None:
        self.cover = cover
        self.cover2x = cover2x
        self.card = card
        self.card2x = card2x
        self.list = list
        self.list2x = list2x
        self.slimcover = slimcover
        self.slimcover2x = slimcover2x

    @staticmethod
    def from_dict(obj: Any) -> 'Covers':
        assert isinstance(obj, dict)
        cover = from_str(obj.get("cover"))
        cover2x = from_str(obj.get("cover@2x"))
        card = from_str(obj.get("card"))
        card2x = from_str(obj.get("card@2x"))
        list = from_str(obj.get("list"))
        list2x = from_str(obj.get("list@2x"))
        slimcover = from_str(obj.get("slimcover"))
        slimcover2x = from_str(obj.get("slimcover@2x"))
        return Covers(cover, cover2x, card, card2x, list, list2x, slimcover, slimcover2x)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cover"] = from_str(self.cover)
        result["cover@2x"] = from_str(self.cover2x)
        result["card"] = from_str(self.card)
        result["card@2x"] = from_str(self.card2x)
        result["list"] = from_str(self.list)
        result["list@2x"] = from_str(self.list2x)
        result["slimcover"] = from_str(self.slimcover)
        result["slimcover@2x"] = from_str(self.slimcover2x)
        return result


class Beatmapset:
    artist: str
    artistunicode: str
    covers: Covers
    creator: str
    favouritecount: int
    hype: None
    id: int
    nsfw: bool
    playcount: int
    previewurl: str
    source: str
    status: str
    title: str
    titleunicode: str
    trackid: Optional[int]
    userid: int
    video: bool

    def __init__(self, artist: str, artistunicode: str, covers: Covers, creator: str, favouritecount: int, hype: None, id: int, nsfw: bool, playcount: int, previewurl: str, source: str, status: str, title: str, titleunicode: str, trackid: Optional[int], userid: int, video: bool) -> None:
        self.artist = artist
        self.artistunicode = artistunicode
        self.covers = covers
        self.creator = creator
        self.favouritecount = favouritecount
        self.hype = hype
        self.id = id
        self.nsfw = nsfw
        self.playcount = playcount
        self.previewurl = previewurl
        self.source = source
        self.status = status
        self.title = title
        self.titleunicode = titleunicode
        self.trackid = trackid
        self.userid = userid
        self.video = video

    @staticmethod
    def from_dict(obj: Any) -> 'Beatmapset':
        assert isinstance(obj, dict)
        artist = from_str(obj.get("artist"))
        artistunicode = from_str(obj.get("artist_unicode"))
        covers = Covers.from_dict(obj.get("covers"))
        creator = from_str(obj.get("creator"))
        favouritecount = from_int(obj.get("favourite_count"))
        hype = from_none(obj.get("hype"))
        id = from_int(obj.get("id"))
        nsfw = from_bool(obj.get("nsfw"))
        playcount = from_int(obj.get("play_count"))
        previewurl = from_str(obj.get("preview_url"))
        source = from_str(obj.get("source"))
        status = from_str(obj.get("status"))
        title = from_str(obj.get("title"))
        titleunicode = from_str(obj.get("title_unicode"))
        trackid = from_union([from_int, from_none], obj.get("track_id"))
        userid = from_int(obj.get("user_id"))
        video = from_bool(obj.get("video"))
        return Beatmapset(artist, artistunicode, covers, creator, favouritecount, hype, id, nsfw, playcount, previewurl, source, status, title, titleunicode, trackid, userid, video)

    def to_dict(self) -> dict:
        result: dict = {}
        result["artist"] = from_str(self.artist)
        result["artist_unicode"] = from_str(self.artistunicode)
        result["covers"] = to_class(Covers, self.covers)
        result["creator"] = from_str(self.creator)
        result["favourite_count"] = from_int(self.favouritecount)
        result["hype"] = from_none(self.hype)
        result["id"] = from_int(self.id)
        result["nsfw"] = from_bool(self.nsfw)
        result["play_count"] = from_int(self.playcount)
        result["preview_url"] = from_str(self.previewurl)
        result["source"] = from_str(self.source)
        result["status"] = from_str(self.status)
        result["title"] = from_str(self.title)
        result["title_unicode"] = from_str(self.titleunicode)
        result["track_id"] = from_union([from_int, from_none], self.trackid)
        result["user_id"] = from_int(self.userid)
        result["video"] = from_bool(self.video)
        return result


class Mode(Enum):
    osu = "osu"


class Beatmap:
    beatmapsetid: int
    difficultyrating: float
    id: int
    mode: Mode
    status: str
    totallength: int
    userid: int
    version: str
    beatmapset: Beatmapset

    def __init__(self, beatmapsetid: int, difficultyrating: float, id: int, mode: Mode, status: str, totallength: int, userid: int, version: str, beatmapset: Beatmapset) -> None:
        self.beatmapsetid = beatmapsetid
        self.difficultyrating = difficultyrating
        self.id = id
        self.mode = mode
        self.status = status
        self.totallength = totallength
        self.userid = userid
        self.version = version
        self.beatmapset = beatmapset

    @staticmethod
    def from_dict(obj: Any) -> 'Beatmap':
        assert isinstance(obj, dict)
        beatmapsetid = from_int(obj.get("beatmapset_id"))
        difficultyrating = from_float(obj.get("difficulty_rating"))
        id = from_int(obj.get("id"))
        mode = Mode(obj.get("mode"))
        status = from_str(obj.get("status"))
        totallength = from_int(obj.get("total_length"))
        userid = from_int(obj.get("user_id"))
        version = from_str(obj.get("version"))
        beatmapset = Beatmapset.from_dict(obj.get("beatmapset"))
        return Beatmap(beatmapsetid, difficultyrating, id, mode, status, totallength, userid, version, beatmapset)

    def to_dict(self) -> dict:
        result: dict = {}
        result["beatmapset_id"] = from_int(self.beatmapsetid)
        result["difficulty_rating"] = to_float(self.difficultyrating)
        result["id"] = from_int(self.id)
        result["mode"] = to_enum(Mode, self.mode)
        result["status"] = from_str(self.status)
        result["total_length"] = from_int(self.totallength)
        result["user_id"] = from_int(self.userid)
        result["version"] = from_str(self.version)
        result["beatmapset"] = to_class(Beatmapset, self.beatmapset)
        return result


class Mod(Enum):
    DT = "DT"
    HD = "HD"
    HR = "HR"
    NF = "NF"


class CurrentUserAttributes:
    pin: None

    def __init__(self, pin: None) -> None:
        self.pin = pin

    @staticmethod
    def from_dict(obj: Any) -> 'CurrentUserAttributes':
        assert isinstance(obj, dict)
        pin = from_none(obj.get("pin"))
        return CurrentUserAttributes(pin)

    def to_dict(self) -> dict:
        result: dict = {}
        result["pin"] = from_none(self.pin)
        return result


class Team(Enum):
    none = "none"


class ScoreMatch:
    slot: int
    team: Team
    matchpass: bool

    def __init__(self, slot: int, team: Team, matchpass: bool) -> None:
        self.slot = slot
        self.team = team
        self.matchpass = matchpass

    @staticmethod
    def from_dict(obj: Any) -> 'ScoreMatch':
        assert isinstance(obj, dict)
        slot = from_int(obj.get("slot"))
        team = Team(obj.get("team"))
        matchpass = from_bool(obj.get("pass"))
        return ScoreMatch(slot, team, matchpass)

    def to_dict(self) -> dict:
        result: dict = {}
        result["slot"] = from_int(self.slot)
        result["team"] = to_enum(Team, self.team)
        result["pass"] = from_bool(self.matchpass)
        return result


class Rank(Enum):
    F = "F"


class Statistics:
    count100: int
    count300: int
    count50: int
    countgeki: int
    countkatu: int
    countmiss: int

    def __init__(self, count100: int, count300: int, count50: int, countgeki: int, countkatu: int, countmiss: int) -> None:
        self.count100 = count100
        self.count300 = count300
        self.count50 = count50
        self.countgeki = countgeki
        self.countkatu = countkatu
        self.countmiss = countmiss

    @staticmethod
    def from_dict(obj: Any) -> 'Statistics':
        assert isinstance(obj, dict)
        count100 = from_int(obj.get("count_100"))
        count300 = from_int(obj.get("count_300"))
        count50 = from_int(obj.get("count_50"))
        countgeki = from_int(obj.get("count_geki"))
        countkatu = from_int(obj.get("count_katu"))
        countmiss = from_int(obj.get("count_miss"))
        return Statistics(count100, count300, count50, countgeki, countkatu, countmiss)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count_100"] = from_int(self.count100)
        result["count_300"] = from_int(self.count300)
        result["count_50"] = from_int(self.count50)
        result["count_geki"] = from_int(self.countgeki)
        result["count_katu"] = from_int(self.countkatu)
        result["count_miss"] = from_int(self.countmiss)
        return result


class Score:
    accuracy: float
    bestid: None
    createdat: datetime
    id: None
    maxcombo: int
    mode: Mode
    modeint: int
    mods: List[Mod]
    passed: bool
    perfect: int
    pp: None
    rank: Rank
    replay: bool
    score: int
    statistics: Statistics
    userid: int
    currentuserattributes: CurrentUserAttributes
    match: ScoreMatch

    def __init__(self, accuracy: float, bestid: None, createdat: datetime, id: None, maxcombo: int, mode: Mode, modeint: int, mods: List[Mod], passed: bool, perfect: int, pp: None, rank: Rank, replay: bool, score: int, statistics: Statistics, userid: int, currentuserattributes: CurrentUserAttributes, match: ScoreMatch) -> None:
        self.accuracy = accuracy
        self.bestid = bestid
        self.createdat = createdat
        self.id = id
        self.maxcombo = maxcombo
        self.mode = mode
        self.modeint = modeint
        self.mods = mods
        self.passed = passed
        self.perfect = perfect
        self.pp = pp
        self.rank = rank
        self.replay = replay
        self.score = score
        self.statistics = statistics
        self.userid = userid
        self.currentuserattributes = currentuserattributes
        self.match = match

    @staticmethod
    def from_dict(obj: Any) -> 'Score':
        assert isinstance(obj, dict)
        accuracy = from_float(obj.get("accuracy"))
        bestid = from_none(obj.get("best_id"))
        createdat = from_datetime(obj.get("created_at"))
        id = from_none(obj.get("id"))
        maxcombo = from_int(obj.get("max_combo"))
        mode = Mode(obj.get("mode"))
        modeint = from_int(obj.get("mode_int"))
        mods = from_list(Mod, obj.get("mods"))
        passed = from_bool(obj.get("passed"))
        perfect = from_int(obj.get("perfect"))
        pp = from_none(obj.get("pp"))
        rank = Rank(obj.get("rank"))
        replay = from_bool(obj.get("replay"))
        score = from_int(obj.get("score"))
        statistics = Statistics.from_dict(obj.get("statistics"))
        userid = from_int(obj.get("user_id"))
        currentuserattributes = CurrentUserAttributes.from_dict(obj.get("current_user_attributes"))
        match = ScoreMatch.from_dict(obj.get("match"))
        return Score(accuracy, bestid, createdat, id, maxcombo, mode, modeint, mods, passed, perfect, pp, rank, replay, score, statistics, userid, currentuserattributes, match)

    def to_dict(self) -> dict:
        result: dict = {}
        result["accuracy"] = to_float(self.accuracy)
        result["best_id"] = from_none(self.bestid)
        result["created_at"] = self.createdat.isoformat()
        result["id"] = from_none(self.id)
        result["max_combo"] = from_int(self.maxcombo)
        result["mode"] = to_enum(Mode, self.mode)
        result["mode_int"] = from_int(self.modeint)
        result["mods"] = from_list(lambda x: to_enum(Mod, x), self.mods)
        result["passed"] = from_bool(self.passed)
        result["perfect"] = from_int(self.perfect)
        result["pp"] = from_none(self.pp)
        result["rank"] = to_enum(Rank, self.rank)
        result["replay"] = from_bool(self.replay)
        result["score"] = from_int(self.score)
        result["statistics"] = to_class(Statistics, self.statistics)
        result["user_id"] = from_int(self.userid)
        result["current_user_attributes"] = to_class(CurrentUserAttributes, self.currentuserattributes)
        result["match"] = to_class(ScoreMatch, self.match)
        return result


class Game:
    id: int
    starttime: datetime
    endtime: datetime
    mode: Mode
    modeint: int
    scoringtype: str
    teamtype: str
    mods: List[Mod]
    beatmap: Beatmap
    scores: List[Score]

    def __init__(self, id: int, starttime: datetime, endtime: datetime, mode: Mode, modeint: int, scoringtype: str, teamtype: str, mods: List[Mod], beatmap: Beatmap, scores: List[Score]) -> None:
        self.id = id
        self.starttime = starttime
        self.endtime = endtime
        self.mode = mode
        self.modeint = modeint
        self.scoringtype = scoringtype
        self.teamtype = teamtype
        self.mods = mods
        self.beatmap = beatmap
        self.scores = scores

    @staticmethod
    def from_dict(obj: Any) -> 'Game':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        starttime = from_datetime(obj.get("start_time"))
        endtime = from_datetime(obj.get("end_time"))
        mode = Mode(obj.get("mode"))
        modeint = from_int(obj.get("mode_int"))
        scoringtype = from_str(obj.get("scoring_type"))
        teamtype = from_str(obj.get("team_type"))
        mods = from_list(Mod, obj.get("mods"))
        beatmap = Beatmap.from_dict(obj.get("beatmap"))
        scores = from_list(Score.from_dict, obj.get("scores"))
        return Game(id, starttime, endtime, mode, modeint, scoringtype, teamtype, mods, beatmap, scores)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["start_time"] = self.starttime.isoformat()
        result["end_time"] = self.endtime.isoformat()
        result["mode"] = to_enum(Mode, self.mode)
        result["mode_int"] = from_int(self.modeint)
        result["scoring_type"] = from_str(self.scoringtype)
        result["team_type"] = from_str(self.teamtype)
        result["mods"] = from_list(lambda x: to_enum(Mod, x), self.mods)
        result["beatmap"] = to_class(Beatmap, self.beatmap)
        result["scores"] = from_list(lambda x: to_class(Score, x), self.scores)
        return result


class Event:
    id: int
    detail: Detail
    timestamp: datetime
    userid: Optional[int]
    game: Optional[Game]

    def __init__(self, id: int, detail: Detail, timestamp: datetime, userid: Optional[int], game: Optional[Game]) -> None:
        self.id = id
        self.detail = detail
        self.timestamp = timestamp
        self.userid = userid
        self.game = game

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        detail = Detail.from_dict(obj.get("detail"))
        timestamp = from_datetime(obj.get("timestamp"))
        userid = from_union([from_int, from_none], obj.get("user_id"))
        game = from_union([Game.from_dict, from_none], obj.get("game"))
        return Event(id, detail, timestamp, userid, game)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["detail"] = to_class(Detail, self.detail)
        result["timestamp"] = self.timestamp.isoformat()
        result["user_id"] = from_union([from_int, from_none], self.userid)
        result["game"] = from_union([lambda x: to_class(Game, x), from_none], self.game)
        return result


class StatusMatch:
    id: int
    starttime: datetime
    endtime: datetime
    name: str

    def __init__(self, id: int, starttime: datetime, endtime: datetime, name: str) -> None:
        self.id = id
        self.starttime = starttime
        self.endtime = endtime
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'StatusMatch':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        starttime = from_datetime(obj.get("start_time"))
        endtime = from_datetime(obj.get("end_time"))
        name = from_str(obj.get("name"))
        return StatusMatch(id, starttime, endtime, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["start_time"] = self.starttime.isoformat()
        result["end_time"] = self.endtime.isoformat()
        result["name"] = from_str(self.name)
        return result


class Country:
    code: str
    name: str

    def __init__(self, code: str, name: str) -> None:
        self.code = code
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'Country':
        assert isinstance(obj, dict)
        code = from_str(obj.get("code"))
        name = from_str(obj.get("name"))
        return Country(code, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_str(self.code)
        result["name"] = from_str(self.name)
        return result


class User:
    avatarurl: str
    countrycode: str
    defaultgroup: str
    id: int
    isactive: bool
    isbot: bool
    isdeleted: bool
    isonline: bool
    issupporter: bool
    lastvisit: datetime
    pmfriendsonly: bool
    profilecolour: None
    username: str
    country: Country

    def __init__(self, avatarurl: str, countrycode: str, defaultgroup: str, id: int, isactive: bool, isbot: bool, isdeleted: bool, isonline: bool, issupporter: bool, lastvisit: datetime, pmfriendsonly: bool, profilecolour: None, username: str, country: Country) -> None:
        self.avatarurl = avatarurl
        self.countrycode = countrycode
        self.defaultgroup = defaultgroup
        self.id = id
        self.isactive = isactive
        self.isbot = isbot
        self.isdeleted = isdeleted
        self.isonline = isonline
        self.issupporter = issupporter
        self.lastvisit = lastvisit
        self.pmfriendsonly = pmfriendsonly
        self.profilecolour = profilecolour
        self.username = username
        self.country = country

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        avatarurl = from_str(obj.get("avatar_url"))
        countrycode = from_str(obj.get("country_code"))
        defaultgroup = from_str(obj.get("default_group"))
        id = from_int(obj.get("id"))
        isactive = from_bool(obj.get("is_active"))
        isbot = from_bool(obj.get("is_bot"))
        isdeleted = from_bool(obj.get("is_deleted"))
        isonline = from_bool(obj.get("is_online"))
        issupporter = from_bool(obj.get("is_supporter"))
        lastvisit = from_datetime(obj.get("last_visit"))
        pmfriendsonly = from_bool(obj.get("pm_friends_only"))
        profilecolour = from_none(obj.get("profile_colour"))
        username = from_str(obj.get("username"))
        country = Country.from_dict(obj.get("country"))
        return User(avatarurl, countrycode, defaultgroup, id, isactive, isbot, isdeleted, isonline, issupporter, lastvisit, pmfriendsonly, profilecolour, username, country)

    def to_dict(self) -> dict:
        result: dict = {}
        result["avatar_url"] = from_str(self.avatarurl)
        result["country_code"] = from_str(self.countrycode)
        result["default_group"] = from_str(self.defaultgroup)
        result["id"] = from_int(self.id)
        result["is_active"] = from_bool(self.isactive)
        result["is_bot"] = from_bool(self.isbot)
        result["is_deleted"] = from_bool(self.isdeleted)
        result["is_online"] = from_bool(self.isonline)
        result["is_supporter"] = from_bool(self.issupporter)
        result["last_visit"] = self.lastvisit.isoformat()
        result["pm_friends_only"] = from_bool(self.pmfriendsonly)
        result["profile_colour"] = from_none(self.profilecolour)
        result["username"] = from_str(self.username)
        result["country"] = to_class(Country, self.country)
        return result


class Status:
    match: StatusMatch
    events: List[Event]
    users: List[User]
    firsteventid: int
    latesteventid: int
    currentgameid: None

    def __init__(self, match: StatusMatch, events: List[Event], users: List[User], firsteventid: int, latesteventid: int, currentgameid: None) -> None:
        self.match = match
        self.events = events
        self.users = users
        self.firsteventid = firsteventid
        self.latesteventid = latesteventid
        self.currentgameid = currentgameid

    @staticmethod
    def from_dict(obj: Any) -> 'Status':
        assert isinstance(obj, dict)
        match = StatusMatch.from_dict(obj.get("match"))
        events = from_list(Event.from_dict, obj.get("events"))
        users = from_list(User.from_dict, obj.get("users"))
        firsteventid = from_int(obj.get("first_event_id"))
        latesteventid = from_int(obj.get("latest_event_id"))
        currentgameid = from_none(obj.get("current_game_id"))
        return Status(match, events, users, firsteventid, latesteventid, currentgameid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["match"] = to_class(StatusMatch, self.match)
        result["events"] = from_list(lambda x: to_class(Event, x), self.events)
        result["users"] = from_list(lambda x: to_class(User, x), self.users)
        result["first_event_id"] = from_int(self.firsteventid)
        result["latest_event_id"] = from_int(self.latesteventid)
        result["current_game_id"] = from_none(self.currentgameid)
        return result


def Statusfromdict(s: Any) -> Status:
    return Status.from_dict(s)


def Statustodict(x: Status) -> Any:
    return to_class(Status, x)
