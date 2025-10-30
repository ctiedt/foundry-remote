# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class TogglePlaylistAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)

    def get_config_rows(self):
        settings = self.get_settings()
        self.id_entry = Adw.EntryRow()
        self.id_entry.set_title("Playlist UUID")
        self.id_entry.set_text(settings.get("playlist", ""))
        self.id_entry.connect("changed", self.on_text_entry)

        return [self.id_entry]

    def on_text_entry(self, entry):
        settings = self.get_settings()
        settings["playlist"] = entry.get_text()
        self.set_settings(settings)
        
    def on_key_down(self) -> None:
        settings = self.get_settings()
        playlist = settings.get("playlist", "")
        self.plugin_base.queue.put({"command": "toggle_playlist", "playlist": playlist})

class PauseMusicAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)
        
    def on_key_down(self) -> None:
        self.plugin_base.queue.put("pause_music")

class PlayNextAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)
        
    def on_key_down(self) -> None:
        self.plugin_base.queue.put("play_next")

class PlayPrevAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)
        
    def on_key_down(self) -> None:
        self.plugin_base.queue.put("play_prev")
  
