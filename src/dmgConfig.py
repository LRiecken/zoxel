import os

filename = "dist/Zoxel-" + (os.environ.get("TRAVIS_TAG") or 'dev') + "-osx.dmg"
appname = 'Zoxel.app'
application = defines.get('app', 'dist/' + appname)
format = defines.get('format', 'UDBZ')
files = [application]
symlinks = {'Applications': '/Applications'}
icon = 'gfx/icons/icon.icns'
icon_locations = {appname: (140, 100), 'Applications': (500, 100)}
background = 'builtin-arrow'
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
sidebar_width = 180
window_rect = ((100, 100), (640, 300))
default_view = 'icon-view'
show_icon_preview = False
include_icon_view_settings = 'auto'
include_list_view_settings = 'auto'
