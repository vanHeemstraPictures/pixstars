import board
import neopixel

NUM_PIXELS = 12
pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS, auto_write=False)
pixels.fill((255, 100, 0))
pixels.show()
