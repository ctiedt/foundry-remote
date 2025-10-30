# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from .actions.MusicControl import TogglePlaylistAction, PauseMusicAction, PlayNextAction, PlayPrevAction
from .actions.CombatControl import BeginCombatAction, EndCombatAction

import json
from queue import Queue
import threading
from websockets.sync.server import serve

QUEUE = Queue()

def handler(ws):
    while True:
        item = QUEUE.get()
        print("Received item ", item)
        if isinstance(item, str):
            ws.send(json.dumps({"command": item}))
        elif isinstance(item, dict):
            ws.send(json.dumps(item))

def ws_thread():
    print("Starting WS Server...")
    with serve(handler, "localhost", 15151) as server:
        server.serve_forever()

class FoundryRemotePlugin(PluginBase):
    def __init__(self):
        super().__init__()

        ## Register actions
        self.toggle_music_holder = ActionHolder(
            plugin_base = self,
            action_base = TogglePlaylistAction,
            action_id = "dev_tiedt_foundry-remote::TogglePlaylistAction",
            action_name = "Toggle Playlist",
        )
        self.add_action_holder(self.toggle_music_holder)

        self.pause_music_holder = ActionHolder(
            plugin_base = self,
            action_base = PauseMusicAction,
            action_id = "dev_tiedt_foundry-remote::PauseMusicAction",
            action_name = "Pause Music",
        )
        self.add_action_holder(self.pause_music_holder)
        
        self.play_next_holder = ActionHolder(
            plugin_base = self,
            action_base = PlayNextAction,
            action_id = "dev_tiedt_foundry-remote::PlayNextAction",
            action_name = "Next Track",
        )
        self.add_action_holder(self.play_next_holder)
        
        self.play_prev_holder = ActionHolder(
            plugin_base = self,
            action_base = PlayPrevAction,
            action_id = "dev_tiedt_foundry-remote::PlayPrevAction",
            action_name = "Previous Track",
        )
        self.add_action_holder(self.play_prev_holder)

        self.begin_combat_holder = ActionHolder(
            plugin_base = self,
            action_base = BeginCombatAction,
            action_id = "dev_tiedt_foundry-remote::BeginCombatAction",
            action_name = "Begin Combat",
        )
        self.add_action_holder(self.begin_combat_holder)

        self.end_combat_holder = ActionHolder(
            plugin_base = self,
            action_base = EndCombatAction,
            action_id = "dev_tiedt_foundry-remote::EndCombatAction",
            action_name = "End Combat",
        )
        self.add_action_holder(self.end_combat_holder)

        # Register plugin
        self.register(
            plugin_name = "FoundryVTT Remote",
            github_repo = "https://github.com/ctiedt/foundry-remote",
            plugin_version = "1.0.0",
            app_version = "1.1.1-alpha"
        )

        self.queue = QUEUE
        self.bg_thread = threading.Thread(target=ws_thread)
        self.bg_thread.start()
        print("Initialized FoundryVTT Remote Plugin")

