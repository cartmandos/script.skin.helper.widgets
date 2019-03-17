#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    script.skin.helper.widgets
    media.py
    all media (mixed) widgets provided by the script
"""
from utils import create_main_entry
from metadatautils import kodi_constants
from operator import itemgetter
from movies import Movies
from tvshows import Tvshows
from songs import Songs
from pvr import Pvr
from albums import Albums
from episodes import Episodes
from random import randint, random
from datetime import date
import xbmc


class Media(object):
    """all media (mixed) widgets provided by the script"""

    ICON_IMAGE_MOVIES = "DefaultMovies.png"
    ICON_IMAGE_TVSHOWS = "DefaultTvShows.png"
    ICON_IMAGE_TAGS = "DefaultTags.png"
    MOVIES_TAGS_PATH = "videodb://movies/tags"
    TVSHOWS_TAGS_PATH = "videodb://tvshows/tags"
    KODI_USER_PLAYLISTS_PATH = "special://videoplaylists/"
    KODI_SKIN_PLAYLISTS_PATH = "special://skin/playlists/"
    PLAYLIST_SORT_OPTIONS = ['Recommended', 'TopPicks', 'Random', 'Recent', 'Year', 'Title']
    YEAR_TODAY_MINUS_FOUR = str(date.today().year - 4)
    FILTER_LAST_THREE_YEARS = {"operator": "greaterthan", "field": "year", "value": YEAR_TODAY_MINUS_FOUR}
    SORT_VOTES = {"method": "votes", "order": "descending"}

    def __init__(self, addon, metadatautils, options):
        """Initializations pass our common classes and the widget options as arguments"""
        self.metadatautils = metadatautils
        self.addon = addon
        self.options = options
        self.movies = Movies(self.addon, self.metadatautils, self.options)
        self.tvshows = Tvshows(self.addon, self.metadatautils, self.options)
        self.songs = Songs(self.addon, self.metadatautils, self.options)
        self.albums = Albums(self.addon, self.metadatautils, self.options)
        self.pvr = Pvr(self.addon, self.metadatautils, self.options)
        self.episodes = Episodes(self.addon, self.metadatautils, self.options)

    def listing(self):
        """main listing with all our media nodes"""
        tag = self.options.get("tag", "")
        exp_setting = self.options["exp_recommended"]
        extended_info_setting = self.options["extended_info"]
        mylist_setting = self.options["mylist"]
        if tag:
            label_prefix = u"%s - " % tag
        else:
            label_prefix = u""

        all_items = [
            (label_prefix + self.addon.getLocalizedString(32011), "inprogress&mediatype=media&tag=%s"
             % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32070),
             "inprogressshowsandmovies&mediatype=media&tag=%s" % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32080),
             "inprogressepisodesandmovies&mediatype=media&tag=%s" % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32005), "recent&mediatype=media&tag=%s"
             % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32078), "recentshowsandmovies&mediatype=media&tag=%s"
             % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32059), "random&mediatype=media&tag=%s"
             % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32079), "randomshowsandmovies&mediatype=media&tag=%s"
             % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32088), "unwatchedshowsandmovies&mediatype=media&tag=%s"
             % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32086), "watchagainshowsandmovies&mediatype=media&tag=%s"
             % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32087), "newrelease&mediatype=media&tag=%s"
             % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32058), "top250&mediatype=media&tag=%s"
             % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32081), "randomtop250&mediatype=media&tag=%s"
             % tag, Media.ICON_IMAGE_MOVIES),
            (label_prefix + self.addon.getLocalizedString(32004), "toprated&mediatype=media&tag=%s"
             % tag, Media.ICON_IMAGE_MOVIES)
        ]
        if exp_setting:
            all_items += [
                (label_prefix + self.addon.getLocalizedString(32084), "recommendedmoviesandshows&mediatype=media&tag=%s"
                 % tag, Media.ICON_IMAGE_MOVIES),
                (label_prefix + self.addon.getLocalizedString(32085), "toppicks&mediatype=media&tag=%s"
                 % tag, Media.ICON_IMAGE_MOVIES)
            ]
            if not tag:
                all_items += [
                    (self.addon.getLocalizedString(32022), "similar&mediatype=media", Media.ICON_IMAGE_MOVIES)
                ]
        if mylist_setting:
            all_items += [
                (self.addon.getLocalizedString(32094), "mylist&mediatype=media", Media.ICON_IMAGE_MOVIES)
            ]
        if not tag:
            all_items += [
                (self.addon.getLocalizedString(32007), "inprogressandrecommended&mediatype=media",
                 Media.ICON_IMAGE_MOVIES),
                (self.addon.getLocalizedString(32060), "inprogressandrandom&mediatype=media", Media.ICON_IMAGE_MOVIES),
                (self.addon.getLocalizedString(32090), "popular&mediatype=media", Media.ICON_IMAGE_MOVIES),
                (self.addon.getLocalizedString(32089), "forgenre&mediatype=media", Media.ICON_IMAGE_MOVIES),
                (xbmc.getLocalizedString(135), "browsegenres&mediatype=media", "DefaultGenres.png"),
                (self.addon.getLocalizedString(32098), "categories&mediatype=media", Media.ICON_IMAGE_MOVIES),
                (self.addon.getLocalizedString(32001), "favourites&mediatype=media", Media.ICON_IMAGE_MOVIES),
                (self.addon.getLocalizedString(32075), "playlistslisting&mediatype=media&movie_label=",
                 Media.ICON_IMAGE_MOVIES),
                (xbmc.getLocalizedString(20459), "tagslisting&mediatype=media", Media.ICON_IMAGE_MOVIES)
            ]
        if extended_info_setting:
            all_items += [
                (self.addon.getLocalizedString(32100) +' - '+ self.addon.getLocalizedString(32090), "extendedpopulartmdb&mediatype=media", Media.ICON_IMAGE_MOVIES),
                (self.addon.getLocalizedString(32101) +' - '+ self.addon.getLocalizedString(32090), "extendedpopulartrakt&mediatype=media", Media.ICON_IMAGE_MOVIES),
                (self.addon.getLocalizedString(32101) +' - '+ self.addon.getLocalizedString(32102), "extendedtrending&mediatype=media", Media.ICON_IMAGE_MOVIES),
                (self.addon.getLocalizedString(32101) +' - '+ self.addon.getLocalizedString(32105), "extendedmostplayed&mediatype=media", Media.ICON_IMAGE_MOVIES),
                (self.addon.getLocalizedString(32101) +' - '+ self.addon.getLocalizedString(32108), "extendedmostwatched&mediatype=media", Media.ICON_IMAGE_MOVIES)
            ]
        return self.metadatautils.process_method_on_list(create_main_entry, all_items)

    def tagslisting(self):
        """get tag listing that are shared with movies and tv shows"""
        all_items = []
        # fetch tag lists
        movies_taglist = self.metadatautils.kodidb.files(Media.MOVIES_TAGS_PATH)
        tvshows_taglist = self.metadatautils.kodidb.files(Media.TVSHOWS_TAGS_PATH)
        # find matched tag
        for movie_tag in movies_taglist:
            for tv_tag in tvshows_taglist:
                if movie_tag["label"] == tv_tag["label"]:
                    details = (
                        movie_tag["label"], "listing&mediatype=media&tag=%s" % movie_tag["label"],
                        Media.ICON_IMAGE_TAGS)
                    all_items.append(create_main_entry(details))
                    # no need to iterate rest of tvshow's tags since match is found -> build entry
                    break
        return all_items

    def playlistslisting(self):
        """get playlists listing
        first set movie_label, then tv_label then return sort entries and call sort method"""
        # add read skin playlists
        tv_label = self.options.get("tv_label")
        movie_label = self.options.get("movie_label")
        if movie_label and tv_label:
            # got both playlist -> let's build sort methods entries from const list
            return [create_main_entry((sort_method, "playlist&mediatype=media&movie_label=%s&tv_label=%s&sort=%s" %
                                       (movie_label, tv_label, sort_method), Media.ICON_IMAGE_MOVIES)) for sort_method
                    in Media.PLAYLIST_SORT_OPTIONS]
        all_items = []
        all_playlists = self.metadatautils.kodidb.files(Media.KODI_USER_PLAYLISTS_PATH) \
                        + self.metadatautils.kodidb.files(Media.KODI_SKIN_PLAYLISTS_PATH)
        for item in all_playlists:
            # replace '&' with [and] -- will get fixed when processed in playlist action
            label = item["label"].replace('&', '[and]')
            if movie_label:
                # got movie playlist -> build playlist entries for tvshows
                details = (item["label"], "playlistslisting&mediatype=media&movie_label=%s&tv_label=%s&sort=" %
                           (movie_label, label), Media.ICON_IMAGE_TVSHOWS)
            else:
                # both labels are empty -> build playlist entries for movies
                details = (item["label"], "playlistslisting&mediatype=media&movie_label=%s" % label,
                           Media.ICON_IMAGE_MOVIES)
            all_items.append(create_main_entry(details))
        return all_items

    def playlist(self):
        """get items in both playlists, sorted by requested sort (defaults to recommended)"""
        # reversing replacing and to ampersand and assign filter dicts
        movie_filter = {"operator": "is", "field": "playlist",
                        "value": self.options.get("movie_label").replace('[and]', '&')}
        tvshow_filter = {"operator": "is", "field": "playlist",
                         "value": self.options.get("tv_label").replace('[and]', '&')}
        sort = self.options.get("sort").lower()
        all_items = self.metadatautils.kodidb.movies(filters=[movie_filter])
        all_items += self.metadatautils.process_method_on_list(self.tvshows.process_tvshow,
                                                               self.metadatautils.kodidb.tvshows(
                                                                   filters=[tvshow_filter]))
        # switch case using dict
        playlist_sort_options = {'recommended': self.playlist_recommended, 'toppicks': self.playlist_toppicks,
                                 'random': self.playlist_random, 'recent': self.playlist_recent,
                                 'year': self.playlist_year, 'title': self.playlist_title}
        if sort and sort in playlist_sort_options:
            return playlist_sort_options[sort](all_items)
        # default case
        else:
            return self.playlist_recommended(all_items)

    def mylist(self):
        """ get mylist """
        filters = []
        if self.options["hide_watched"]:
            filters.append(kodi_constants.FILTER_UNWATCHED)
        filters.append({"operator": "contains", "field": "tag", "value": 'mylist'})
        all_items = self.metadatautils.kodidb.movies(filters=filters)
        all_items += self.metadatautils.process_method_on_list(self.tvshows.process_tvshow,
                                                               self.metadatautils.kodidb.tvshows(filters=filters))
        return sorted(all_items, key=itemgetter("dateadded"), reverse=True)[:self.options["limit"]]

    def categories(self):
        """not ready"""
        all_items = []
        all_items += self.browsegenres()
        all_items += [{"art": {}, "label": "movies", "title": xbmc.getLocalizedString(342),
                       "file": "videodb://movies/titles/",
                       "isFolder": True, "IsPlayable": "false", "thumbnail": Media.ICON_IMAGE_MOVIES, "type": "categorie"}]
        all_items += [{"art": {}, "label": "tvshows", "title": xbmc.getLocalizedString(20343),
                       "file": "videodb://tvshows/titles/",
                       "isFolder": True, "IsPlayable": "false", "thumbnail": Media.ICON_IMAGE_TVSHOWS, "type": "categorie"}]
        all_items += [
            {"art": {}, "label": "topratedmovies", "title": self.addon.getLocalizedString(32083),
             "file": u"plugin://script.skin.helper.widgets/?action=toprated&mediatype=movies&limit=100",
             "isFolder": True, "IsPlayable": "false", "thumbnail": Media.ICON_IMAGE_MOVIES, "type": "categorie"}]
        all_items += [
            {"art": {}, "label": "topratedtvshows", "title": self.addon.getLocalizedString(32097),
             "file": u"plugin://script.skin.helper.widgets/?action=toprated&mediatype=tvshows&limit=100",
             "isFolder": True, "IsPlayable": "false", "thumbnail": Media.ICON_IMAGE_TVSHOWS, "type": "categorie"}]
        all_items += [
            {"art": {}, "label": "recentlyadded", "title": self.addon.getLocalizedString(32078),
             "file": u"plugin://script.skin.helper.widgets/?action=recentshowsandmovies&mediatype=media&limit=100",
             "isFolder": True, "IsPlayable": "false", "thumbnail": Media.ICON_IMAGE_MOVIES, "type": "categorie"}]
        all_items += [
            {"art": {}, "label": "newrelease", "title": self.addon.getLocalizedString(32087),
             "file": u"plugin://script.skin.helper.widgets/?action=newrelease&mediatype=media&limit=100",
             "isFolder": True, "IsPlayable": "false", "thumbnail": Media.ICON_IMAGE_MOVIES, "type": "categorie"}]
        all_items += [
            {"art": {}, "label": "popular", "title": self.addon.getLocalizedString(32090),
             "file": u"plugin://script.skin.helper.widgets/?action=popular&mediatype=media&limit=100",
             "isFolder": True, "IsPlayable": "false", "thumbnail": Media.ICON_IMAGE_MOVIES, "type": "categorie"}]
        return sorted(all_items, key=lambda k: random())[:self.options["limit"]]

    def favourites(self):
        """get favourite media"""
        from favourites import Favourites
        self.options["mediafilter"] = "media"
        return Favourites(self.addon, self.metadatautils, self.options).favourites()

    def favourite(self):
        """synonym to favourites"""
        return self.favourites()

    def forgenre(self):
        """ get random movies and tv shows for given shared genre"""
        genre = self.options.get("genre", "")
        movie_genres = self.metadatautils.kodidb.genres("movie")
        tvshow_genres = self.metadatautils.kodidb.genres("tvshow")
        if not genre:
            media_genres = []
            for movie_genre in movie_genres:
                for tvshow_genre in tvshow_genres:
                    if movie_genre["label"] == tvshow_genre["label"]:
                        media_genres.append(movie_genre["label"])
                        break
            if media_genres:
                # get random genre from matched genres
                genre = media_genres[randint(0, len(media_genres) - 1)]
        all_items = []
        if genre:
            for item in self.tvshows.get_genre_tvshows(genre, self.options["hide_watched"], self.options["limit"]):
                item["extraproperties"] = {"genretitle": genre, "originalpath": item["file"]}
                all_items.append(item)
            # proccess tvshows before adding movies
            all_items = self.metadatautils.process_method_on_list(self.tvshows.process_tvshow, all_items)
            for item in self.movies.get_genre_movies(genre, self.options["hide_watched"], self.options["limit"]):
                item["extraproperties"] = {"genretitle": genre, "originalpath": item["file"]}
                all_items.append(item)
        # return the list sorted random capped by limit
        return sorted(all_items, key=lambda k: random())[:self.options["limit"]]

    def toprated(self):
        """get top rated mixed media"""
        all_items = []
        all_items += self.movies.toprated()
        all_items += self.tvshows.toprated()
        return sorted(all_items, key=lambda k: random())[:self.options["limit"]]

    def recommendedmoviesandshows(self):
        """ get recommended movies and tv shows """
        return self.sort_by_recommended(self.get_items_for_recommended())

    def toppicks(self):
        """ get top picks movies and tv shows based on profile reference pooling """
        return self.sort_by_recommended(self.get_items_for_recommended(), True)

    def popular(self):
        """get popular movies and tv shows based on new and most voted, arranged by date added and year of release"""
        filters = []
        if self.options["hide_watched"]:
            filters.append(kodi_constants.FILTER_UNWATCHED)
        all_items = self.metadatautils.kodidb.movies(
            filters=filters + [Media.FILTER_LAST_THREE_YEARS],
            sort=Media.SORT_VOTES,
            limits=(0, self.options["limit"]))
        all_items += self.metadatautils.process_method_on_list(self.tvshows.process_tvshow,
                                                               self.metadatautils.kodidb.tvshows(
                                                                   filters=filters + [Media.FILTER_LAST_THREE_YEARS],
                                                                   sort=Media.SORT_VOTES,
                                                                   limits=(0, self.options["limit"])))
        # first sort by dateadded to mix tv and movies and maybe better release indication, then verify by year
        return sorted(sorted(all_items, key=itemgetter("dateadded"), reverse=True)
                      [:self.options["limit"]], key=itemgetter("year"), reverse=True)

    def unwatchedshowsandmovies(self):
        """ get random unwatched tvshows and movies"""
        filters = [kodi_constants.FILTER_UNWATCHED]
        if self.options.get("tag"):
            filters.append({"operator": "contains", "field": "tag", "value": self.options["tag"]})
        all_items = self.metadatautils.kodidb.movies(sort=kodi_constants.SORT_RANDOM, filters=filters,
                                                     limits=(0, self.options["limit"]))
        all_items += self.metadatautils.process_method_on_list(self.tvshows.process_tvshow,
                                                               self.metadatautils.kodidb.tvshows(
                                                                   sort=kodi_constants.SORT_RANDOM, filters=filters,
                                                                   limits=(0, self.options["limit"])))
        return sorted(all_items, key=lambda k: random())[:self.options["limit"]]

    def newrelease(self):
        """ get newly released movies and tvshows based on added recently and released in last 3 years"""
        filters = [Media.FILTER_LAST_THREE_YEARS]
        if self.options["hide_watched"]:
            filters.append(kodi_constants.FILTER_UNWATCHED)
        if self.options.get("tag"):
            filters.append({"operator": "contains", "field": "tag", "value": self.options["tag"]})
        # first we take all recently added and released in last 3 years capped by limit
        all_items = self.metadatautils.kodidb.movies(sort=kodi_constants.SORT_DATEADDED, filters=filters,
                                                     limits=(0, self.options["limit"]))
        all_items += self.metadatautils.process_method_on_list(
            self.tvshows.process_tvshow,
            self.metadatautils.kodidb.tvshows(sort=kodi_constants.SORT_DATEADDED, filters=filters,
                                              limits=(0, self.options["limit"])))
        # randomize to let tvshows mix with movies due to likeliness of being same year, and return sorted by year
        return sorted(sorted(all_items, key=lambda k: random()), key=itemgetter("year"), reverse=True)[
               :self.options["limit"]]

    def recent(self):
        """ get recently added media """
        all_items = self.movies.recent()
        all_items += self.albums.recent()
        all_items += self.songs.recent()
        all_items += self.episodes.recent()
        all_items += self.pvr.recordings()
        return sorted(all_items, key=itemgetter("dateadded"), reverse=True)[:self.options["limit"]]

    def recentshowsandmovies(self):
        """ get recently added movies and tvshows """
        all_items = self.movies.recent()
        all_items += self.tvshows.recent()
        return sorted(all_items, key=itemgetter("dateadded"), reverse=True)[:self.options["limit"]]

    def random(self):
        """ get random media """
        all_items = self.movies.random()
        all_items += self.tvshows.random()
        all_items += self.albums.random()
        all_items += self.songs.random()
        all_items += self.episodes.random()
        all_items += self.pvr.recordings()
        return sorted(all_items, key=lambda k: random())[:self.options["limit"]]

    def randomshowsandmovies(self):
        """ get random tv shows and movies """
        all_items = self.movies.random()
        all_items += self.tvshows.random()
        return sorted(all_items, key=lambda k: random())[:self.options["limit"]]

    def inprogress(self):
        """ get in progress media """
        all_items = self.movies.inprogress()
        all_items += self.episodes.inprogress()
        all_items += self.pvr.recordings()
        return sorted(all_items, key=itemgetter("lastplayed"), reverse=True)[:self.options["limit"]]

    def inprogressepisodesandmovies(self):
        """ get in progress episodes and movies """
        all_items = self.movies.inprogress()
        all_items += self.episodes.inprogress()
        return sorted(all_items, key=itemgetter("lastplayed"), reverse=True)[:self.options["limit"]]

    def inprogressshowsandmovies(self):
        """ get in-progress/next episodes AS TV Shows and in-progress movies """
        all_items = self.movies.inprogress()
        all_items += self.tvshows.nextshows()
        return sorted(all_items, key=itemgetter("lastplayed"), reverse=True)[:self.options["limit"]]

    def inprogressandrecommended(self):
        """ get recommended and in progress media """
        all_items = self.inprogress()
        all_titles = [item["title"] for item in all_items]
        for item in self.recommended():
            if item["title"] not in all_titles:
                all_items.append(item)
        return all_items[:self.options["limit"]]

    def inprogressandrandom(self):
        """ get in progress AND random movies """
        all_items = self.inprogress()
        all_ids = [item["movieid"] for item in all_items]
        for item in self.random():
            if item["movieid"] not in all_ids:
                all_items.append(item)
        return all_items[:self.options["limit"]]

    def watchagainshowsandmovies(self):
        """ get random recently watched movies and tv shows """
        filters = [kodi_constants.FILTER_WATCHED]
        if self.options.get("tag"):
            filters.append({"operator": "contains", "field": "tag", "value": self.options["tag"]})
        all_items = self.metadatautils.kodidb.movies(sort=kodi_constants.SORT_LASTPLAYED,
                                                     filters=filters,
                                                     limits=(0, self.options["limit"]))
        all_items += self.metadatautils.process_method_on_list(
            self.tvshows.process_tvshow,
            self.metadatautils.kodidb.tvshows(sort=kodi_constants.SORT_LASTPLAYED,
                                              filters=filters + [kodi_constants.FILTER_INPROGRESS],
                                              filtertype="or",
                                              limits=(0, self.options["limit"])))
        return sorted(all_items, key=lambda k: random())[:self.options["limit"]]

    def top250(self):
        """ get imdb top250 movies and tvshows in library by top250 rand """
        return sorted(self.get_top_250(), key=itemgetter("top250_rank"))[:self.options["limit"]]

    def randomtop250(self):
        """ get random imdb top250 movies and tvshows in library """
        return sorted(self.get_top_250(), key=lambda k: random())[:self.options["limit"]]

    def extendedpopulartmdb(self):
        """gets popular movies and tvshows from tmdb"""
        all_items = []
        all_items += self.movies.extendedpopulartmdb()
        all_items += self.tvshows.extendedpopulartmdb()
        return sorted(all_items, key=itemgetter("extendedindex"))[:self.options["limit"]]

    def extendedpopulartrakt(self):
        """gets popular movies and tvshows from trakt"""
        all_items = []
        all_items += self.movies.extendedpopulartrakt()
        all_items += self.tvshows.extendedpopulartrakt()
        return sorted(all_items, key=itemgetter("extendedindex"))[:self.options["limit"]]

    def extendedtrending(self):
        """gets popular movies and tvshows from trakt"""
        all_items = []
        all_items += self.movies.extendedtrending()
        all_items += self.tvshows.extendedtrending()
        return sorted(all_items, key=itemgetter("extendedindex"))[:self.options["limit"]]

    def extendedmostplayed(self):
        """gets most played movies and tvshows from trakt"""
        all_items = []
        all_items += self.movies.extendedmostplayed()
        all_items += self.tvshows.extendedmostplayed()
        return sorted(all_items, key=itemgetter("extendedindex"))[:self.options["limit"]]

    def extendedmostwatched(self):
        """gets most watched movies and tvshows from trakt"""
        all_items = []
        all_items += self.movies.extendedmostwatched()
        all_items += self.tvshows.extendedmostwatched()
        return sorted(all_items, key=itemgetter("extendedindex"))[:self.options["limit"]]

    def browsegenres(self):
        """special entry which can be used to create custom genre listings
            returns each genre with poster/fanart artwork properties from 5
            random movies/tvshows in the genre."""
        # find matches
        movie_genres = self.metadatautils.kodidb.genres("movie")
        tvshow_genres = self.metadatautils.kodidb.genres("tvshow")
        media_genres = []
        for movie_genre in movie_genres:
            for tvshow_genre in tvshow_genres:
                if movie_genre["label"] == tvshow_genre["label"]:
                    media_genres.append(movie_genre["label"])
                    break
        # build genres
        all_items = []
        for genre in media_genres:
            all_items.append(self.process_genre(genre))
        return all_items

    def process_genre(self, genre):
        """method to create genre listitem from genre's label"""
        genre_json = {"art": {}, "label": genre, "title": genre,
                      "file": u"plugin://script.skin.helper.widgets/?action=forgenre&mediatype=media&genre=%s" % genre,
                      "isFolder": True, "IsPlayable": "false", "thumbnail": "DefaultGenre.png", "type": "genre"}
        # randomly select fanart/poster from tvshows OR movies
        flip_coin = randint(0, 1)
        if flip_coin:
            genre_items = self.movies.get_genre_movies(genre, False, 5, kodi_constants.SORT_RANDOM)
        else:
            genre_items = self.tvshows.get_genre_tvshows(genre, False, 5, kodi_constants.SORT_RANDOM)
        if genre_items:
            for count, item in enumerate(genre_items):
                genre_json["art"]["poster.%s" % count] = item["art"].get("poster", "")
                genre_json["art"]["fanart.%s" % count] = item["art"].get("fanart", "")
                if "fanart" not in genre_json["art"]:
                    # set genre's primary fanart image to first movie fanart
                    genre_json["art"]["fanart"] = item["art"].get("fanart", "")
        return genre_json

    def get_top_250(self):
        """ get all imdb top250 movies and tv shows in library """
        all_items = self.movies.top250()
        all_items += self.tvshows.top250()
        return all_items

    def get_items_for_recommended(self):
        """get all items for recommended and top picks methods"""
        filters = [kodi_constants.FILTER_UNWATCHED]
        # get all unwatched, not in-progess movies & tvshows
        if self.options.get("tag"):
            filters.append({"operator": "contains", "field": "tag", "value": self.options["tag"]})
        movies = self.metadatautils.kodidb.movies(filters=filters)
        filters.append({"operator": "false", "field": "inprogress",
                        "value": ""})
        tvshows = self.metadatautils.process_method_on_list(self.tvshows.process_tvshow,
                                                            self.metadatautils.kodidb.tvshows(filters=filters))
        return movies + tvshows

    def get_recently_watched_item(self):
        """ get a random recently watched movie or tvshow """
        num_recent_similar = (self.options["num_recent_similar"] + 1) / 2
        recent_items = self.metadatautils.kodidb.movies(sort=kodi_constants.SORT_LASTPLAYED,
                                                        filters=[kodi_constants.FILTER_WATCHED],
                                                        limits=(0, num_recent_similar))
        recent_items += self.metadatautils.kodidb.tvshows(sort=kodi_constants.SORT_LASTPLAYED,
                                                          filters=[kodi_constants.FILTER_WATCHED,
                                                                   kodi_constants.FILTER_INPROGRESS],
                                                          filtertype="or",
                                                          limits=(0, num_recent_similar))
        if recent_items:
            return recent_items[randint(0, len(recent_items) - 1)]

    def similar(self):
        """ get similar movies and similar tvshows for given imdbid"""
        if self.options["exp_recommended"]:
            # get ref item, and check if movie
            ref_item = self.get_recently_watched_item()
            is_ref_movie = False
            if ref_item:
                is_ref_movie = "uniqueid" in ref_item
            # create list of all items
            if self.options["hide_watched_similar"]:
                all_items = self.metadatautils.kodidb.movies(filters=[kodi_constants.FILTER_UNWATCHED])
                all_items += self.metadatautils.process_method_on_list(
                    self.tvshows.process_tvshow, self.metadatautils.kodidb.tvshows(
                        filters=[kodi_constants.FILTER_UNWATCHED,
                                 {"operator": "false", "field": "inprogress", "value": ""}]))
            else:
                all_items = self.metadatautils.kodidb.movies()
                all_items += self.metadatautils.process_method_on_list(
                    self.tvshows.process_tvshow, self.metadatautils.kodidb.tvshows())
            if ref_item:
                if is_ref_movie:
                    # define sets for speed
                    set_genres = set(ref_item["genre"])
                    set_directors = set(ref_item["director"])
                    set_writers = set(ref_item["writer"])
                    set_cast = set([x["name"] for x in ref_item["cast"][:5]])
                    # get similarity score for all items
                    for item in all_items:
                        if "uniqueid" in item:
                            # if item is also movie, check if it's the ref_item
                            if item["title"] == ref_item["title"] and item["year"] == ref_item["year"]:
                                # don't rank the reference movie
                                similarscore = 0
                            else:
                                # otherwise, use movie method for score
                                similarscore = self.movies.get_similarity_score(ref_item, item,
                                                                                set_genres=set_genres,
                                                                                set_directors=set_directors,
                                                                                set_writers=set_writers,
                                                                                set_cast=set_cast)
                        else:
                            # if item isn't movie, use mixed method
                            similarscore = self.get_similarity_score(ref_item, item)
                        # set extraproperties
                        item["similarscore"] = similarscore
                        item["extraproperties"] = {"similartitle": ref_item["title"], "originalpath": item["file"]}
                else:
                    # define sets for speed
                    set_genres = set(ref_item["genre"])
                    set_cast = set([x["name"] for x in ref_item["cast"][:10]])
                    # get similarity score for all items
                    for item in all_items:
                        if "uniqueid" not in item:
                            # if item is also tvshow, check if it's the ref_item
                            if item["title"] == ref_item["title"] and item["year"] == ref_item["year"]:
                                # don't rank the reference movie
                                similarscore = 0
                            else:
                                # otherwise, use tvshow method for score
                                similarscore = self.tvshows.get_similarity_score(ref_item, item,
                                                                                 set_genres=set_genres,
                                                                                 set_cast=set_cast)
                        else:
                            # if item isn't tvshow, use mixed method
                            similarscore = self.get_similarity_score(ref_item, item)
                        # set extraproperties
                        item["similarscore"] = similarscore
                        item["extraproperties"] = {"similartitle": ref_item["title"], "originalpath": item["file"]}
                # return list sorted by score and capped by limit
                return sorted(all_items, key=itemgetter("similarscore"), reverse=True)[:self.options["limit"]]
        else:
            all_items = self.movies.similar()
            all_items += self.tvshows.similar()
            all_items += self.albums.similar()
            all_items += self.songs.similar()
            return sorted(all_items, key=lambda k: random())[:self.options["limit"]]

    def sort_by_recommended(self, all_items, probe=False):
        if probe:
            all_refs = self.get_references_by_profile()
        else:
            all_refs = self.get_references_last_played()
        # average scores together for every item
        if all_refs:
            for item in all_items:
                similarscore = 0
                for ref_item in all_refs:
                    # add all similarscores for item
                    if "uniqueid" in ref_item and "uniqueid" in item:
                        # use movies method if both items are movies
                        similarscore += self.movies.get_similarity_score(ref_item, item)
                    elif "uniqueid" in ref_item or "uniqueid" in item:
                        # use media method if only one item is a movie
                        similarscore += self.get_similarity_score(ref_item, item)
                    else:
                        # use tvshows method if neither items are movies
                        similarscore += self.tvshows.get_similarity_score(ref_item, item)

                item["recommendedscore"] = similarscore / (1 + item["playcount"]) / len(all_refs)
            # return sorted list capped by limit
            return sorted(all_items, key=itemgetter("recommendedscore"), reverse=True)[:self.options["limit"]]

    def get_references_last_played(self):
        """ sort list of mixed movies/tvshows by recommended score"""
        # get recently watched items
        num_recent_similar = self.options["num_recent_similar"]
        all_refs = []
        all_refs += self.metadatautils.kodidb.tvshows(sort=kodi_constants.SORT_LASTPLAYED,
                                                      filters=[kodi_constants.FILTER_WATCHED],
                                                      limits=(0, num_recent_similar))
        all_refs += self.metadatautils.kodidb.movies(sort=kodi_constants.SORT_LASTPLAYED,
                                                     filters=[kodi_constants.FILTER_WATCHED],
                                                     limits=(0, num_recent_similar))
        return all_refs

    def get_references_by_profile(self):
        """ sort list of mixed movies/tvshows by recommended score"""
        # get recently watched items
        num_recent_similar = self.options["num_recent_similar"] + 1
        # get random values for pools
        first_pool = randint(1, num_recent_similar - 1)
        second_pool = randint(1, num_recent_similar - first_pool)

        # first pool
        all_refs_movies = self.metadatautils.kodidb.movies(sort=kodi_constants.SORT_RANDOM,
                                                           filters=[{"operator": "contains", "field": "tag",
                                                                     "value": 'mylist'}],
                                                           limits=(0, first_pool))
        all_refs_tvshows = self.metadatautils.kodidb.tvshows(sort=kodi_constants.SORT_RANDOM,
                                                             filters=[{"operator": "contains", "field": "tag",
                                                                       "value": 'mylist'}],
                                                             limits=(0, first_pool))
        # second pool
        all_refs_movies += self.metadatautils.kodidb.movies(sort=kodi_constants.SORT_RANDOM,
                                                            filters=[{"operator": "greaterthan", "field": "userrating",
                                                                      "value": '6'},
                                                                     {"operator": "doesnotcontain", "field": "tag",
                                                                      "value": 'mylist'}],
                                                            limits=(0, second_pool))
        all_refs_tvshows += self.metadatautils.kodidb.tvshows(sort=kodi_constants.SORT_RANDOM,
                                                              filters=[
                                                                  {"operator": "greaterthan", "field": "userrating",
                                                                   "value": '6'},
                                                                  {"operator": "doesnotcontain", "field": "tag",
                                                                   "value": 'mylist'}],
                                                              limits=(0, second_pool))
        # fill what's left
        # note: might be overlap but probably better to allow some than add calculation time & space in memory
        third_pool = num_recent_similar * 2 - (len(all_refs_movies) + len(all_refs_tvshows))
        if third_pool > 0 and (len(all_refs_movies) + len(all_refs_tvshows)) > 0:
            priority_factor = int(len(all_refs_movies) / (len(all_refs_movies) + len(all_refs_tvshows)))
            third_pool_movies = third_pool * priority_factor
            third_pool_tvshows = third_pool - third_pool_movies

            all_refs_movies += self.metadatautils.kodidb.movies(sort=kodi_constants.SORT_LASTPLAYED,
                                                                filters=[kodi_constants.FILTER_WATCHED],
                                                                limits=(0, third_pool_movies))
            all_refs_tvshows += self.metadatautils.kodidb.tvshows(sort=kodi_constants.SORT_LASTPLAYED,
                                                                  filters=[kodi_constants.FILTER_WATCHED],
                                                                  limits=(0, third_pool_tvshows))
        return all_refs_movies + all_refs_tvshows

    def playlist_recommended(self, all_items):
        return self.sort_by_recommended(all_items)

    def playlist_toppicks(self, all_items):
        return self.sort_by_recommended(all_items, True)

    def playlist_random(self, all_items):
        return sorted(all_items, key=lambda k: random())[:self.options["limit"]]

    def playlist_recent(self, all_items):
        return sorted(all_items, key=itemgetter("dateadded"), reverse=True)[:self.options["limit"]]

    def playlist_year(self, all_items):
        return sorted(all_items, key=itemgetter("year"), reverse=True)[:self.options["limit"]]

    def playlist_title(self, all_items):
        return sorted(all_items, key=itemgetter("title"))[:self.options["limit"]]

    @staticmethod
    def get_similarity_score(ref_item, other_item):
        """get a similarity score (0-.75) between movie and tvshow"""
        set_genres = set(ref_item["genre"])
        set_cast = set([x["name"] for x in ref_item["cast"][:5]])
        # calculate individual scores for contributing factors
        # genre_score = (number of matching genres) / (number of unique genres between both)
        genre_score = float(len(set_genres.intersection(other_item["genre"]))) / \
                      len(set_genres.union(other_item["genre"]))
        # cast_score is normalized by fixed amount of 5, and scaled up nonlinearly
        cast_score = (float(len(set_cast.intersection([x["name"] for x in other_item["cast"][:5]]))) / 5) ** (1. / 2)
        # rating_score is "closeness" in rating, scaled to 1
        if ref_item["rating"] and other_item["rating"] and abs(ref_item["rating"] - other_item["rating"]) < 3:
            rating_score = 1 - abs(ref_item["rating"] - other_item["rating"]) / 3
        else:
            rating_score = 0
        # year_score is "closeness" in release year, scaled to 1 (0 if not from same decade)
        if ref_item["year"] and other_item["year"] and abs(ref_item["year"] - other_item["year"]) < 10:
            year_score = 1 - abs(ref_item["year"] - other_item["year"]) / 10
        else:
            year_score = 0
        # calculate overall score using weighted average
        similarscore = .5 * genre_score + .1 * cast_score + .025 * rating_score + .025 * year_score
        return similarscore
