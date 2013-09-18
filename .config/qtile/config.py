#!/usr/bin/env python
# encoding: utf-8
# Note that since qtile configs are just python scripts, you can check for
# syntax and runtime errors by just running this file as is from the command
# line, e.g.:
#
# python config.py

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

# The screens variable contains information about what bars are drawn where on
# each screen. If you have multiple screens, you'll need to construct multiple
# Screen objects, each with whatever widgets you want.
#
# Below is a screen with a top bar that contains several basic qtile widgets.
screens = [Screen(top = bar.Bar([
        # This is a list of our virtual desktops.
        widget.GroupBox(urgent_alert_method='text'),

        # A prompt for spawning processes or switching groups. This will be
        # invisible most of the time.
        widget.Prompt(),

        # Current window name.
        widget.WindowName(),
        widget.Volume(),
        widget.Battery(
            energy_now_file='charge_now',
            energy_full_file='charge_full',
            power_now_file='current_now',
        ),
        widget.Systray(),
        widget.Clock('%Y-%m-%d %a %I:%M %p'),
    ], 30)) # our bar is 30px high
]

# Super_L (the Windows key) is typically bound to mod4 by default, so we use
# that here.
mod = "mod4"

# The keys variable contains a list of all of the keybindings that qtile will
# look through each time there is a key pressed.
keys = [
    # Log out; note that this doesn't use mod4: that's intentional in case mod4
    # gets hosed (which happens if you unplug and replug your usb keyboard
    # sometimes, or on system upgrades). This way you can still log back out
    # and in gracefully.
    Key([mod, "shift"], "q", lazy.shutdown()),

    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "h", lazy.layout.previous()),
    Key([mod], "l", lazy.layout.previous()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod, "shift"], "Return",lazy.layout.toggle_split()),
    Key(["mod1"], "Tab", lazy.nextlayout()),
    Key([mod], "c", lazy.window.kill()),
    # Key([mod], "n", lazy.layout.normalize()),
    # Key([mod], "f", lazy.layout.maximize()),

    # interact with prompts
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "g", lazy.switchgroup()),

    Key([mod, "shift"], "r", lazy.restart()),

    # start specific apps
    Key([mod], "control","f", lazy.spawn("firefox")),
    Key([mod], "Return", lazy.spawn("urxvt")),

    # Change the volume if your keyboard has special volume keys.
    Key(
        [], "XF86AudioRaiseVolume",
        lazy.spawn("amixer -c 0 -q set Master 2dB+")
    ),
    Key(
        [], "XF86AudioLowerVolume",
        lazy.spawn("amixer -c 0 -q set Master 2dB-")
    ),
    Key(
        [], "XF86AudioMute",
        lazy.spawn("amixer -c 0 -q set Master toggle")
    ),

    # Also allow changing volume the old fashioned way.
    Key([mod], "equal", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([mod], "minus", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
]

# This allows you to drag windows around with the mouse if you want.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groupName = ["1≯web", "2≯dev", "3≯hack", "4≯bgrun", "5≯video"]
groups = []

for i in ["1", "2", "3", "4", "5"]:
    groups.append(Group(groupName[int(i)-1]))
    keys.append(
        Key([mod], i, lazy.group[groupName[int(i)-1]].toscreen())
    )
    keys.append(
        Key([mod, "shift"], i, lazy.window.togroup(groupName[int(i)-1]))
    )

# Two basic layouts.
layouts = [
    layout.Stack(stacks=2, border_width=1),
    layout.Max(),
]

# vim: tabstop=4 shiftwidth=4 expandtab