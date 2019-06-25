import dbus
from functools import reduce


class SpotifyDBus(object):
    """Spotify DBus items here.
    Define basic DBus keywords for Spotify DBus.
    """

    def __init__(self):
        """Init SpotifyDBus with basic keywords."""
        self.name = 'org.mpris.MediaPlayer2.spotify'
        self.path = '/org/mpris/MediaPlayer2'
        self.interface = 'org.freedesktop.DBus.Properties'
        self.method = 'Get'
        self.meta_interface = 'org.mpris.MediaPlayer2.Player'
        self.metadata_label = 'Metadata'
        self.metadata_title = 'xesam:title'
        self.metadata_album = 'xesam:album'
        self.metadata_artist = 'xesam:artist'

    def get_metadata(self):
        """If all good, return Spotify's DBus Metadata.
        Metadata contains current song's information which is a dict.

        Metadata:
            album: Album name.
            artist: Artist name.
            title: Song name.
        """
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object(self.name, self.path)
        iface = dbus.Interface(spotify_bus, self.interface)
        method_get = iface.get_dbus_method(self.method)
        return method_get(self.meta_interface, self.metadata_label)

    def get_keywords(self):
        """Pick keywords from DBus."""
        metadata = self.get_metadata()
        title = metadata[dbus.String(self.metadata_title)][:]
        album = metadata[dbus.String(self.metadata_album)][:]
        artist = reduce(lambda x, y: x[:] + ' ' + y[:],
                        metadata[dbus.String(self.metadata_artist)][:])[:]
        return '%s %s %s' % (title, album, artist)
