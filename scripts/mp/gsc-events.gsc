init() {
    setDvar("scr_allowFileIo", "1");

    level thread onPlayerConnected();
    level thread onPlayerSay();

    level thread onKillcam();
    level thread onKillcamEnd();

    level.onplayerdisconnect = ::onPlayerDisconnected;
    level.onplayerkilled = ::onPlayerKilled;

}

onPlayerConnected() {
    for(;;) {
        level waittill( "connected", player );
        thread call_event("player_connected", player.name);

        player thread onJoinedSpectators();
        player thread onPlayerSpawned();
        player thread onWeaponChange();
        player thread onPlayerDeath();
        player thread onJoinedTeam();
    }
}

onPlayerSpawned() {
    for(;;) {
        self waittill( "spawned_player" );
        thread call_event("player_spawned", self.name);
    }
}

onPlayerDeath() {
    for(;;) {
        self waittill( "death" );
        thread call_event("player_death", self.name);
    }
}

onJoinedSpectators() {
    for (;;) {
        self waittill( "joined_spectators" );
        thread call_event("joined_spectators", self.name);
    }
}

onPlayerKilled(einflictor, attacker, idamage, smeansofdeath, sweapon, vdir, shitloc, psoffsettime, deathanimduration) {
    thread call_event("player_killed", self.name, attacker.name, smeansofdeath, sweapon, shitloc);
}

onPlayerDisconnected() {
    thread call_event("player_disconnected", self.name);
}

onWeaponChange() {
    for(;;) {
        self waittill( "weapon_change", weapon );
        thread call_event("weapon_change", self.name, weapon);
    }
}

onPlayerSay() {
    for(;;) {
        level waittill( "say", message, player );
        thread call_event("player_say", player.name, message);
    }
}

onMenuResponse() {
    for (;;) {
        self waittill( "menuresponse", menu, response );
        thread call_event("menu_response", self.name, menu, response);
    }
}

onJoinedTeam() {
    for(;;) {
        self waittill( "joined_team" );
        thread call_event("joined_team", self.name, self.pers["team"]);
    }
}


onKillcam() {
    for(;;) {
        level waittill( "play_final_killcam" );
        thread call_event("killcam_start");
    }
}

onKillcamEnd() {
    for(;;) {
        level waittill( "final_killcam_done" );
        thread call_event("killcam_end");
    }
}

call_event( event, arg1, arg2, arg3, arg4, arg5 ) {
    if (arg1 == undefined || arg1 == "" ) {
        event_log = "{ \"event\": \"" + event + "\" }";
    } 

    else if (arg2 == undefined || arg2 == "") {
        event_log = "{ \"event\": \"" + event + "\", \"args\": [\"" + arg1 + "\"] }";
    } 

    else if (arg3 == undefined || arg3 == "" ) {
        event_log = "{ \"event\": \"" + event + "\", \"args\": [\"" + arg1 + "\", \"" + arg2 + "\"] }";
    }

    else if (arg4 == undefined || arg4 == "" ) {
        event_log = "{ \"event\": \"" + event + "\", \"args\": [\"" + arg1 + "\", \"" + arg2 + "\", \"" + arg3 + "\"] }";
    }

    else if (arg5 == undefined || arg5 == "" ) {
        event_log = "{ \"event\": \"" + event + "\", \"args\": [\"" + arg1 + "\", \"" + arg2 + "\", \"" + arg3 + "\", \"" + arg4 + "\"] }";
    }

    else {
        event_log = "{ \"event\": \"" + event + "\", \"args\": [\"" + arg1 + "\", \"" + arg2 + "\", \"" + arg3 + "\", \"" + arg4 + "\", \"" + arg5 + "\"] }";
    }
    
    file = fs_fopen("event_" + event + ".jsonl", "append");
    fs_write(file, event_log + "\n");
    fs_fclose(file);

    println("^2[event]: " + event_log);
}
