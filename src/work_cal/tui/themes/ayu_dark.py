from textual.theme import Theme

ayu_dark = Theme(
    name="ayu_dark",
    primary="#59c2ff",         # blue
    secondary="#73b8ff",       # cyan
    accent="#ff8f40",          # orange
    foreground="#bfbdb6",      # foreground
    background="#0f1419",      # background
    success="#aad94c",         # green
    warning="#e6b450",         # yellow
    error="#f07178",           # red
    surface="#131721",         # black
    panel="#2d3640",           # dark_gray
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#59c2ff",
        "input-selection-background": "#2d3640",
        "scrollbar-background": "#131721",
        "scrollbar-thumb": "#5c6773",
        "border": "#5c6773",
        "outline": "#59c2ff",
        "dialog-background": "#131721",
        "button-background": "#2d3640",
        "button-background-hover": "#5c6773",
        "input-background": "#2d3640",
        "input-background-focus": "#131721",
        "header-background": "#131721",
        "footer-background": "#131721",
        "tab-active-background": "#2d3640",
        "tab-inactive-background": "#131721",
        "link": "#73b8ff",
        "link-hover": "#59c2ff",
        "text-muted": "#5c6773",
        "text-accent": "#d2a6ff",
        "highlight": "#e6b450",
    },
)
