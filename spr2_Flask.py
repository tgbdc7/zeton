import pyglet
import datetime

window = pyglet.window.Window(300, 200, caption='Pyglet Clock')

czas_warna = pyglet.text.Label('--:--',
                               font_name='Arial',
                               font_size=30,
                               anchor_x='center',
                               anchor_y='center',
                               x=window.width / 2,
                               y=window.height / 2,
                               )


@window.event
def on_draw():
    window.clear()
    czas_warna.draw()


def update_time(dt):
    czas_warna.text = datetime.datetime.now().strftime('%M:%S')


pyglet.clock.schedule_interval(update_time, 1)

pyglet.app.run()
