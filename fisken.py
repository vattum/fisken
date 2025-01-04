"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import random
import arcade

SPRITE_SCALING_PLAYER = 0.15
SPRITE_SCALING_FISH = 0.1
FISH_COUNT = 200

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Fisken"

# Speed limit
MAX_SPEED_PLAYER = 7
MAX_SPEED_FISHES = 2

# How fast we accelerate
ACCELERATION_RATE = 0.4

# How fast to slow down after we let off the key
FRICTION = 0.05


class Player(arcade.Sprite):
    """Player Class"""

    def update(self):
        """Move the player"""
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.angle = -self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
            self.change_x = 0  # Zero x speed
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
            self.change_x = 0

        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
            self.change_y = 0

class Fish(arcade.Sprite):
    """
    This class represents the fishes on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def reset_pos(self):

        # Reset the fish to a random spot above the screen
        self.center_y = random.randrange(50, SCREEN_HEIGHT - 50)
        self.center_x = random.randrange(-50*FISH_COUNT*MAX_SPEED_FISHES, -100)

    def update(self):

        # Move the fish
        self.center_x += round(MAX_SPEED_FISHES * SPRITE_SCALING_FISH / self.scale)

        # See if the fish has gone to the right of the screen.
        # If so, reset it.
        if self.left > SCREEN_WIDTH:
            self.reset_pos()

class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None
        self.fish_sprite_list = None

        self.score = 0
        
        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        arcade.set_background_color(arcade.color.COAL)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """Set up the game variables. Call to re-start the game."""
        # Create your sprites and sprite lists here

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.fish_sprite_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("bilder/fisk1.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = SCREEN_WIDTH - 100
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        # Create the fishes
        for i in range(FISH_COUNT):

            # Create the fish instance
            fish = Fish("bilder/fisk2.png", SPRITE_SCALING_FISH * random.uniform(0.5, 2))

            # Position the fish
            fish.reset_pos()

            # Add the fish to the lists
            self.fish_sprite_list.append(fish)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Draw all the sprites.
        self.player_list.draw()        
        self.fish_sprite_list.draw()

        # Display speed
        #arcade.draw_text(
        #   f"X Speed: {self.player_sprite.change_x:6.3f}", 10, 50, arcade.color.BLACK
        #
        #arcade.draw_text(
        #   f"Y Speed: {self.player_sprite.change_y:6.3f}", 10, 70, arcade.color.BLACK
        #
        
        # Put the text on the screen.
        output = f"Poäng: {self.score}"
        arcade.draw_text(output, 10, 10, arcade.color.BLACK, 14)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # Add some friction
        if self.player_sprite.change_x > FRICTION:
            self.player_sprite.change_x -= FRICTION
        elif self.player_sprite.change_x < -FRICTION:
            self.player_sprite.change_x += FRICTION
        else:
            self.player_sprite.change_x = 0

        if self.player_sprite.change_y > FRICTION:
            self.player_sprite.change_y -= FRICTION
        elif self.player_sprite.change_y < -FRICTION:
            self.player_sprite.change_y += FRICTION
        else:
            self.player_sprite.change_y = 0

        # Apply acceleration based on the keys pressed
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y += ACCELERATION_RATE
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y += -ACCELERATION_RATE
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x += -ACCELERATION_RATE
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x += ACCELERATION_RATE

        if self.player_sprite.change_x > MAX_SPEED_PLAYER:
            self.player_sprite.change_x = MAX_SPEED_PLAYER
        elif self.player_sprite.change_x < -MAX_SPEED_PLAYER:
            self.player_sprite.change_x = -MAX_SPEED_PLAYER
        if self.player_sprite.change_y > MAX_SPEED_PLAYER:
            self.player_sprite.change_y = MAX_SPEED_PLAYER
        elif self.player_sprite.change_y < -MAX_SPEED_PLAYER:
            self.player_sprite.change_y = -MAX_SPEED_PLAYER

        # Move the player
        self.player_list.update()

        self.fish_sprite_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.fish_sprite_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for fish in hit_list:
            fish.remove_from_sprite_lists()
            self.score += 1

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        #elif key == arcade.key.LEFT:
        #    self.left_pressed = True
        #elif key == arcade.key.RIGHT:
        #    self.right_pressed = True

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        print(x, y, button)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """Main function"""
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
