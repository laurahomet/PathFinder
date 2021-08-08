#------------------------------------------------------
# Name: Path Finder A* Constants
# Author: Laura Homet Garcia
# Date: May 11 2021
#------------------------------------------------------

GRID = {
	"rows"  : 40,
	"width" : 800
}

SPOT_SZ = GRID["width"] // GRID["rows"]

BLUE         = (0, 128, 255)
TURQUOISE 	 = (64, 224, 208)
ORANGE 		 = (255, 178, 102)
LIGHT_ORANGE = (255, 204, 153)
DARK_ORANGE  = (204, 102, 0)
WHITE 		 = (255, 255, 255)
BLACK 		 = (0, 0, 0)
GREY         = (128, 128, 128)

RGB = {
	"start"   : BLUE,
	"end"     : TURQUOISE, 
	"open"    : ORANGE,
	"closed"  : LIGHT_ORANGE,
	"empty"   : WHITE,
	"barrier" : BLACK,
	"path"    : DARK_ORANGE,
	"line"    : GREY
}

MAP = {
	"empty"   : 0,
	"start"   : 1,
	"end"     : 2,
	"barrier" : 8,
}
