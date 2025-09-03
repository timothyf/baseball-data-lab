from dataclasses import dataclass, field

FOOTER_TEXT = {
    1: {
        'text': 'Code by: Timothy Fisher',
        'fontsize': 24 },
    2: {
        'text': 'Color Coding Compares to League Average By Pitch',
        'fontsize': 16 },
    3: {
        'text': 'Data: MLB, Fangraphs\nImages: MLB, ESPN',
        'fontsize': 24 }
}

pitch_colors = {
    ## Fastballs ##
    'FF': {'color': '#FF007D', 'name': '4-Seam Fastball'},
    'FA': {'color': '#FF007D', 'name': 'Fastball'},
    'SI': {'color': '#98165D', 'name': 'Sinker'},
    'FC': {'color': '#BE5FA0', 'name': 'Cutter'},

    ## Offspeed ##
    'CH': {'color': '#F79E70', 'name': 'Changeup'},
    'FS': {'color': '#FE6100', 'name': 'Splitter'},
    'SC': {'color': '#F08223', 'name': 'Screwball'},
    'FO': {'color': '#FFB000', 'name': 'Forkball'},

    ## Sliders ##
    'SL': {'color': '#67E18D', 'name': 'Slider'},
    'ST': {'color': '#1BB999', 'name': 'Sweeper'},
    'SV': {'color': '#376748', 'name': 'Slurve'},

    ## Curveballs ##
    'KC': {'color': '#311D8B', 'name': 'Knuckle Curve'},
    'CU': {'color': '#3025CE', 'name': 'Curveball'},
    'CS': {'color': '#274BFC', 'name': 'Slow Curve'},
    'EP': {'color': '#648FFF', 'name': 'Eephus'},

    ## Others ##
    'KN': {'color': '#867A08', 'name': 'Knuckleball'},
    'PO': {'color': '#472C30', 'name': 'Pitch Out'},
    'UN': {'color': '#9C8975', 'name': 'Unknown'},
}


@dataclass
class FontConfig:
    default_family: str = 'DejaVu Sans'
    default_size: int = 12
    title_size: int = 20
    axes_size: int = 16

    font_properties: dict = field(init=False)

    def __post_init__(self):
        # Setup the font properties for easy access
        self.font_properties = {
            'default': {'family': self.default_family, 'size': self.default_size},
            'titles': {'family': self.default_family, 'size': self.title_size, 'fontweight': 'bold'},
            'axes': {'family': self.default_family, 'size': self.axes_size},
        }
