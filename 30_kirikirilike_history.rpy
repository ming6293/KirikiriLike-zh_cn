# KirikiriLike — 独立的历史（回想）界面
#
# 在 init 999 覆盖自带 `history` 界面（因此会胜过默认定义，默认定义为 init 0）。
# 它完全独立：不通过 `game_menu` 路由，因此显示时没有左侧导航菜单/分隔线，
# 也不需要额外美术资源（只在场景背景上叠加一层纯色暗色蒙版）。
#
# 历史内的滚轮行为：
#   * 滚轮向上  -> 向上滚动到更早的消息（由 vpgrid/viewport 处理）
#   * 滚轮向下 -> 滚向更新的消息，然后到底部时关闭
#
# 若要禁用此覆盖并恢复自带游戏菜单历史，请删除此单一文件。

init 999 python:

    def _kkl_hs(project_style, fallback_style):
        # 选择项目自带样式或库的回退样式，
        # 每次渲染都会重新求值，因此 kkl.history_use_project_styles 可实时生效。
        return project_style if kkl.history_use_project_styles else fallback_style


    class _KKLHistoryWheelDown(Action, DictEquality):
        """Scroll History down, returning to dialogue only at the bottom."""

        def __call__(self):
            scroll = Scroll("kkl_history_scroll", "vertical increase")

            if scroll.get_sensitive():
                return scroll()

            return Return()()


init 999 screen history():

    tag menu

    ## 避免预加载此界面，因为它可能非常大。
    predict False

    ## 背景：场景图像（无分隔线）加暗色蒙版。复刻自带游戏菜单的变暗效果，
    ## 但不使用 "gui/overlay/game_menu.png" 分隔线。
    add gui.game_menu_background
    add Solid("#000000cc")

    ## 标题。
    label _("History"):
        style _kkl_hs("game_menu_label", "kkl_history_title")

    ## 回想列表。frame 填满屏幕（减去内边距），使 vpgrid/viewport
    ## 具有可滚动的有限高度。
    frame:
        style _kkl_hs("game_menu_outer_frame", "kkl_history_outer")
        background None
        xfill True
        yfill True

        if gui.history_height:

            vpgrid:
                id "kkl_history_scroll"
                cols 1
                yinitial 1.0

                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True

                side_yfill True

                for h in _history_list:
                    window:
                        style _kkl_hs("history_window", "kkl_history_window")

                        has fixed:
                            yfit True

                        if h.who:
                            label h.who:
                                style _kkl_hs("history_name", "kkl_history_name")
                                substitute False
                                if "color" in h.who_args:
                                    text_color h.who_args["color"]

                        $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                        text what:
                            style _kkl_hs("history_text", "kkl_history_text")
                            substitute False

                if not _history_list:
                    label _("The dialogue history is empty."):
                        style _kkl_hs("history_label", "kkl_history_label")

        else:

            viewport:
                id "kkl_history_scroll"
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True

                side_yfill True

                vbox:
                    for h in _history_list:
                        window:
                            style _kkl_hs("history_window", "kkl_history_window")

                            has fixed:
                                yfit True

                            if h.who:
                                label h.who:
                                    style _kkl_hs("history_name", "kkl_history_name")
                                    substitute False
                                    if "color" in h.who_args:
                                        text_color h.who_args["color"]

                            $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                            text what:
                                style _kkl_hs("history_text", "kkl_history_text")
                                substitute False

                    if not _history_list:
                        label _("The dialogue history is empty."):
                            style _kkl_hs("history_label", "kkl_history_label")

    ## 返回游戏。
    textbutton _("Return"):
        style _kkl_hs("return_button", "kkl_history_return")
        action Return()

    ## 滚轮向下会在仍有更多内容时滚向更新条目，然后在底部下一次
    ## 向下滚动时返回游戏。
    if kkl.enable_wheelnav and kkl.history_closes_on_wheeldown:
        key kkl.wheel_down_key action _KKLHistoryWheelDown()


## ---------------------------------------------------------------------------
## 回退样式，仅当 kkl.history_use_project_styles == False 时使用
## （即项目没有标准 history_*/game_menu_* 样式）。它们基于 Ren'Py 的基础
## gui 样式，因此可独立工作。
## ---------------------------------------------------------------------------

style kkl_history_title is gui_label:
    xpos 50
    ysize 120
style kkl_history_title_text is gui_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style kkl_history_outer is empty:
    top_padding 120
    bottom_padding 30

style kkl_history_window is empty:
    xfill True
    ysize gui.history_height

style kkl_history_name is gui_label:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width
style kkl_history_name_text is gui_label_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style kkl_history_text is gui_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign

style kkl_history_label is gui_label:
    xfill True
style kkl_history_label_text is gui_label_text:
    xalign 0.5

style kkl_history_return is gui_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30
style kkl_history_return_text is gui_button_text
