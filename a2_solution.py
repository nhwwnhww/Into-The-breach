from a2_support import *
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional, Callable

# MODEL ---------------------------------------------------------------------#


class Tile:
    """    
    An abstract class providing base functionality for all tiles
    """
    NAME = TILE_NAME
    SYMBOL = TILE_SYMBOL

    def __str__(self) -> str:
        return self.SYMBOL

    def __repr__(self) -> str:
        return f"{self.get_tile_name()}()"

    def get_tile_name(self) -> str:
        """
        (str) Returns the name of the tile
        """
        return self.NAME

    def is_blocking(self) -> bool:
        """
        (bool) Return True if the tile type is blocking, otherwise False
        """
        return False


class Ground(Tile):
    """
    A basic tile that represents ground in the game, which is never blocking
    """
    NAME = GROUND_NAME
    SYMBOL = GROUND_SYMBOL


class Mountain(Tile):
    """
    A basic tile that represents a mountain in the game, which 
    is always blocking
    """
    NAME = MOUNTAIN_NAME
    SYMBOL = MOUNTAIN_SYMBOL

    def is_blocking(self) -> bool:
        return True


class Building(Tile):
    """
    A basic tile that represents a building in the game,
    which is blocking until it is destroyed
    """
    NAME = BUILDING_NAME
    STARTING_HEALTH = 3 

    def __init__(self, initial_health: int = STARTING_HEALTH) -> None:
        """
        Construct a building

        Args:
            (str) initial_health: the initial health of the building.
                                  Precondition: 
                                  0 <= initial_health <= MAX_BUILDING_HEALTH
        """
        self._health = initial_health

    def __repr__(self) -> str:
        return self.get_tile_name() + f"({self._health})"

    def __str__(self) -> str:
        return str(self._health)

    def damage(self, damage: int) -> None:
        """
        Reduce building's health by the given damage, the building's health
        is capped between 0 and MAX_BUILDING_HEALTH

        Args:
            (int) damage: the amount of damage is dealt to the building.
        """
        if self.is_destroyed():
            return

        self._health -= damage
        if self._health > MAX_BUILDING_HEALTH:
            self._health = MAX_BUILDING_HEALTH

        if self._health <= 0:
            self._health = 0

    def is_destroyed(self) -> bool:
        """
        (bool) Return True if the building is destroyed, otherwise False
        """
        return self._health <= 0

    def is_blocking(self) -> bool:
        return self._health > 0


class Board():
    """
    Class representing the board of all tiles in the current game state
    """
    def __init__(self, board: list[list[str]]) -> None:
        """
        Construct all instances on the board with given symbols

        Args:
            (list[list[str]]) board: a sequence of each row of tile symbols.
                                     Preconditions: all rows are of the same 
                                     length, and len(board) > 0.
        """
        self._height = len(board)
        self._width = len(board[0])

        # Construct board of instances based on symbols
        self._board = []
        for row in board:
            new_row = []
            for symbol in row:
                if symbol == GROUND_SYMBOL:
                    new_row.append(Ground())
                elif symbol == MOUNTAIN_SYMBOL:
                    new_row.append(Mountain())
                else:
                    new_row.append(Building(int(symbol)))
            self._board.append(new_row)

    def __repr__(self) -> str:
        return (
            "Board(" + 
            str([[str(tile) for tile in row] for row in self._board]) +
            ")"
        ) 

    def __str__(self) -> str:
        return "\n".join(
            [
                "".join([
                    str(self._board[row][col]) for col in range(self._width)
                ]) for row in range(self._height)
            ]
        )

    def get_dimensions(self) -> tuple[int, int]:
        """
        (tuple[int, int]) Return the dimensions of the board (#rows, #columns)
        """
        return (self._height, self._width)

    def get_tile(self, position: tuple[int, int]) -> Tile:
        """
        (Tile) Return the instances of the tile in the given (row, column) 
        position on the board
        """
        row, column = position
        return self._board[row][column]

    def get_buildings(self) -> dict[tuple[int, int], Building]:
        """
        (dict[tuple[int, int], Building]) Return a dictionary of building
        instances, where the key is the position and the value is the instance
        """
        buildings = {}
        for row in range(self._height):
            for col in range(self._width):
                tile = self.get_tile((row, col))
                if tile.get_tile_name() == BUILDING_NAME:
                    buildings[(row, col)] = tile
        return buildings


class Entity:
    """
    An abstract class providing base functionality for all entities
    """
    NAME = "Entity"
    SYMBOL = "E"
    FRIENDLY = False

    def __init__(self, position: tuple[int, int], initial_health: int, 
                 speed: int, strength: int) -> None:
        """
        Construct an entity

        Args:
            (tuple[int, int]) position: entity's position upon initializing
            (int) initial_health: entity's health upon initializing
            (int) speed: entity's speed upon initializing
            (int) strength: entity's strength upon initializing
        """
        self._position = position
        self._health = initial_health
        self._speed = speed
        self._strength = strength

    def __str__(self) -> str:
        row, col = self.get_position()
        return ",".join(
            [
                str(property) for property in [
                    self.SYMBOL,
                    row,
                    col,
                    self._health,
                    self._speed,
                    self._strength
                ]
            ]
        )

    def __repr__(self) -> str:
        return (self.NAME
            + f"({self._position}, {self._health}, {self._speed}, "
              f"{self._strength})")

    def get_symbol(self) -> str:
        """
        (str) Return the symbol that represents this entity
        """
        return self.SYMBOL

    def get_name(self) -> str:
        """
        (str) Return the name that represents this entity
        """
        return self.NAME

    def get_position(self) -> tuple[int, int]:
        """
        (str) Return the current position of this entity
        """
        return self._position

    def set_position(self, pos: tuple[int, int]) -> None:
        """
        Change the current position of this entity to the given position

        Args:
            (tuple[int, int]) pos: New position of entity.
        """
        self._position = pos

    def get_health(self) -> int:
        """
        (str) Return the current health of this entity
        """
        return self._health

    def get_speed(self) -> int:
        """
        (str) Return the speed of this entity
        """
        return self._speed

    def get_strength(self) -> int:
        """
        (str) Return the strength of this entity
        """
        return self._strength

    def damage(self, damage: int) -> None:
        """
        Apply damage to this entity in accordance with game rules.

        Args:
            (int) damage: the amount of damage dealt to this entity
        """
        if not self.is_alive():
            return

        self._health -= damage
        if self._health <= 0:
            self._health = 0

    def is_alive(self) -> bool:
        """
        (bool) Return True if this entity is alive otherwise False
        """
        return self._health > 0

    def is_friendly(self) -> bool:
        """
        (bool) Return True if this entity is friendly, otherwise False
        """
        return self.FRIENDLY

    def get_targets(self) -> list[tuple[int, int]]:
        """
        (list[tuple[int, int]]) Return a sequence of positions that represents 
        the positions that this entity will attack.
        """
        return [
            (self._position[0] + offset[0], self._position[1] + offset[1])
            for offset in PLUS_OFFSETS
        ]

    def attack(self, entity: "Entity") -> None:
        """
        Make this entity attack another entity

        Args:
            (Entity) entity: The entity to be attacked by this entity
        """
        entity.damage(self._strength)


class Mech(Entity):
    """
    Abstract class providing extended base functionality of player controlled 
    mech entities.
    """
    NAME = MECH_NAME
    SYMBOL = MECH_SYMBOL
    FRIENDLY = True

    def __init__(
        self, 
        position: tuple[int, int], 
        initial_health: int, 
        speed: int, 
        strength: int
    ) -> None:
        super().__init__(position, initial_health, speed, strength)
        self._moved = False
        self._position = position

    def set_position(self, pos: tuple[int, int]) -> None:
        self._position = pos

    def enable(self) -> None:
        """
        Sets the mech to be active
        """
        self._moved = False

    def disable(self) -> None:
        """
        Sets the mech to not be active
        """
        self._moved = True

    def is_active(self) -> bool:
        """
        (bool) Return True if this entity is active, otherwise False
        """
        return not self._moved


class TankMech(Mech):
    """
    A player controlled entity that attacks horizontally with a long range.
    """
    NAME = TANK_NAME
    SYMBOL = TANK_SYMBOL

    def get_targets(self) -> list[tuple[int, int]]:
        return [
            (self._position[0], self._position[1] + ((i + 1) * offset))
            for i in range(TANK_RANGE)
            for offset in (1, -1)
        ]


class HealMech(Mech):
    """
    A player controlled entity that attacks immediately adjascent tiles. 
    Instead of doing damage, attacks do nothing to enemies and heal mechs
    and buildings. 
    """
    NAME = HEAL_NAME
    SYMBOL = HEAL_SYMBOL

    def __init__(
        self, 
        position: tuple[int, int], 
        initial_health: int, 
        speed: int, 
        strength: int
    ) -> None:
        super().__init__(position, initial_health, speed, -strength)

    def __repr__(self) -> str:
        return (self.NAME
            + f"({self._position}, {self._health}, {self._speed}, " \
            f"{-self._strength})") 

    def __str__(self) -> str:
        row, col = self.get_position()
        return ",".join(
            [
                str(property) for property in [
                    self.SYMBOL,
                    row,
                    col,
                    self._health,
                    self._speed,
                    -self._strength
                ]
            ]
        )

    def attack(self, entity: Entity) -> None:
        # Heal only friendlies
        if entity.is_friendly():
            super().attack(entity)


class Enemy(Entity):
    """
    Abstract class providing extended base functionality for computer 
    controlled enemy entities
    """
    NAME = ENEMY_NAME
    SYMBOL = ENEMY_SYMBOL

    def __init__(
        self, 
        position: tuple[int, int], 
        initial_health: int, 
        speed: int, 
        strength: int
    ) -> None:
        super().__init__(position, initial_health, speed, strength)
        self._objective = self._position

    def get_objective(self) -> tuple[int, int]:
        """
        (tuple[int, int]) Returns the enemy's objective position
        """
        return self._objective

    def update_objective(self, entities: list[Entity], 
                         buildings: dict[tuple[int, int], Building]) -> None:
        """
        Updates the enemy's objective to a position decided upon based on 
        a set of entities and buildings from the game. 

        Args:
            entities (list[Entity]): List of entities from the game. 
                                     Precondition: Will be in descending 
                                     priotity order.
            buildings (dict[tuple[int, int], Building]): Dictionary mapping 
                                                         positions to building 
                                                         instances occupying 
                                                         those positions
        """
        self._objective = self._position


class Scorpion(Enemy):
    """
    An enemy that attacks in a "Plus" pattern with moderate range, 
    and wants to move towards the mech with the greatest health.
    """
    NAME = SCORPION_NAME
    SYMBOL = SCORPION_SYMBOL

    def get_targets(self) -> list[tuple[int, int]]:
        # Moderate range melee attack for low damage
        return [
            (
                self._position[0] + ((i + 1) * offset[0]),
                self._position[1] + ((i + 1) * offset[1]),
            )
            for i in range(SCORPION_RANGE)
            for offset in PLUS_OFFSETS
        ]

    def update_objective(self, entities: list[Entity], 
                         buildings: dict[tuple[int, int], Building]) -> None:
        # Scorpion targets freindly with highest health
        max_health = 0
        for candidate in entities:
            if candidate.is_friendly() \
                and (candidate.get_health() > max_health):
                max_health = candidate.get_health()
                self._objective = candidate.get_position()


class Firefly(Enemy):
    """
    An enemy that attacks vertically with a long range, and wants to move
    towards the building with the lowest health that is not destroyed.
    """
    NAME = FIREFLY_NAME
    SYMBOL = FIREFLY_SYMBOL

    def get_targets(self) -> list[tuple[int, int]]:
        # Long range vertical attack
        return [
            (self._position[0] + ((i + 1) * offset), self._position[1])
            for i in range(TANK_RANGE)
            for offset in (1, -1)
        ]

    def update_objective(self, entities: list[Entity], 
                         buildings: dict[tuple[int, int], Building]) -> None:
        # Firefly targets building with lowest health
        min_health = -1
        for building_pos in buildings:
            candidate_health = int(str(buildings[building_pos]))
            if ((0 < candidate_health <= min_health or min_health < 0) or
                #Tuples compare lexiographically, choose bottom right if tie
                (candidate_health == min_health 
                and building_pos >= self._objective)): 
                min_health = candidate_health
                self._objective = building_pos

# Maps symbols to the constructor of the relevent entity
ENTITY_MAP = {
    entity_class.SYMBOL: entity_class
    for entity_class in [TankMech, HealMech, Scorpion, Firefly]
}

class BreachModel():
    """
    Class that models the logical state of a game of Into The Breach
    """
    def __init__(self, board: Board, entities: list[Entity]) -> None:
        """
        Constructs a new model of a game of Into The Breach

        Args:
            board (Board): Initial board state
            entities (list[Entity]): Initial list of entities present.
                                     Precondition: Entities appear 
                                     in descending priority order
        """
        self._board = board
        self._entities = entities

        self._can_save = True

    def __str__(self) -> str:
        model_representation = str(self._board) + "\n"

        # Add entities to string
        for entity in self._entities:
            model_representation += "\n" + str(entity)

        return model_representation

    def get_board(self) -> Board:
        """
        (Board) Returns current board state
        """
        return self._board

    def get_entities(self) -> list[Entity]:
        """
        (list[Entity]) Returns list of current entities in descending priority 
        order
        """
        return self._entities

    def _has_friendly(self) -> bool:
        """
        (bool) Returns true if there is a friendly entity still alive. Returns 
        false otherwise
        """
        for entity in self._entities:
            if entity.is_friendly():
                return True
        return False

    def _has_enemies(self) -> bool:
        """
        (bool) Returns true if there is a friendly enemy still alive. Returns 
        false otherwise
        """
        for entity in self._entities:
            if not entity.is_friendly():
                return True
        return False

    def _has_buildings(self) -> bool:
        """
        (bool) Returns true if there is a building still standing. Returns 
        false otherwise
        """
        for building in self._board.get_buildings().values():
            if not building.is_destroyed():
                return True
        return False

    def has_won(self) -> bool:
        """
        (bool) Returns true if the player has won. Returns false otherwise
        """
        return (
                self._has_friendly() and 
                self._has_buildings() and 
                not self._has_enemies()
        )

    def has_lost(self) -> bool:
        """
        (bool) Returns true if the player has lost. Returns false otherwise
        """
        return not (self._has_friendly() and self._has_buildings())

    def entity_positions(self) -> dict[tuple[int, int], Entity]:
        """
        (dict[tuple[int, int], Entity]) Returns a dictionary containing all 
        entities, indexed by entity position.
        """
        return {e.get_position(): e for e in self._entities}

    def _can_move_entity(self, 
                         entity: Entity, position: tuple[int, int]) -> bool:
        """
        Returns whether an entity can be moved to a given position.

        Args:
            entity (Entity): An entity in the game
            position (tuple[int, int]): A position on the game board

        Returns:
            bool: True if the given entity can move to the specified position,
                  False otherwise.
        """
        if self._board.get_tile(position).is_blocking():
            return False

        if position in self.entity_positions():
            return False

        return (
            0
            <= get_distance(self, entity.get_position(), position)
            <= entity.get_speed()
        )

    def get_valid_movement_positions(self, 
                                     entity: Entity) -> list[tuple[int, int]]:
        """
        Returns the set of positions that an entity is allowed to move to on the 
        game board.

        Args:
            entity (Entity): An entity in the game

        Returns:
            list[tuple[int, int]]: List containing positions that the given 
                                   entity can move to. Ordered such that 
                                   positions in higher rows appear before 
                                   positions in lower rows, and positions in 
                                   columns further left appear before positions 
                                   in columns further right.
        """
        coords = []
        height, width = self._board.get_dimensions()
        for row in range(height):
            for col in range(width):
                candidate = (row, col)
                if self._can_move_entity(entity, candidate):
                    coords.append(candidate)

        return coords

    def attempt_move(self, entity: Entity, position: tuple[int, int]) -> None:
        """
        Moves a given entity to the specified position if it is active and 
        allowed to move there.

        Args:
            entity (Entity): An entity to move
            position (tuple[int, int]): Position to move entity to
        """
        if (
            entity.is_friendly()
            and entity.is_active()
            and position in self.get_valid_movement_positions(entity)
        ):
            entity.set_position(position)
            entity.disable()

            # Record movement
            self._can_save = False

    def ready_to_save(self) -> bool:
        """
        (bool) Returns true if the current game state can be written to a file.
        Returns false otherwise.
        """
        return self._can_save

    def assign_objectives(self) -> None:
        """
        Updates the objectives of each enemy in the game, based on the current 
        state of the game.
        """
        for entity in self._entities:
            if not entity.is_friendly():
                entity.update_objective(self._entities, 
                                        self._board.get_buildings())

    def move_enemies(self) -> None:
        """
        Moves every enemy in the game in priority order to the valid movement 
        location that minimises the distance between the enemy 
        and its objective
        """
        for entity in self._entities:
            if entity.is_friendly():
                continue

            # Determine position to move to
            target_pos = entity.get_position() # NOTE: If no paths, dont move
            min_dist = float("inf")
            for candidate in self.get_valid_movement_positions(entity):
                candidate_distance = get_distance(
                    self, entity.get_objective(), candidate
                )
                if (
                    (0 <= candidate_distance <= min_dist) or 
                    (candidate_distance == min_dist and candidate >= target_pos)
                ):  # NOTE: If tie go bottom, then right
                    target_pos = candidate
                    min_dist = candidate_distance

            entity.set_position(target_pos)

    def make_attack(self, entity: Entity) -> None:
        """
        Makes an entity perform an attack against every tile it is targetting

        Args:
            entity (Entity): Entity to perform the attacks
        """
        for target in entity.get_targets():
            max_height, max_width = self._board.get_dimensions()
            # Check Bounds:
            if 0 <= target[0] < max_height and 0 <= target[1] < max_width:
                # Damage buildings according to strength of entity
                target_tile = self._board.get_tile(target)
                if target_tile.get_tile_name() == BUILDING_NAME:
                    target_tile.damage(entity.get_strength())

                # Attack any entities according to class behavior
                if target in self.entity_positions():
                    entity.attack(self.entity_positions()[target])

    def end_turn(self) -> None:
        """
        Causes all entities to attack in priorty order, then reassigns enemy 
        objectives and moves enemies in priority order
        """
        # Make attacks in order
        for entity in self._entities:
            if entity.is_alive():  # Note death interrupts attack
                self.make_attack(entity)

        # Clear dead entities (preserve order)
        old_entities = self._entities
        self._entities = []
        for entity in old_entities:
            if entity.is_alive():
                self._entities.append(entity)

        # Move enemies
        self.assign_objectives()
        self.move_enemies()

        # Set up for player turn
        for entity in self._entities:
            if entity.is_friendly():
                entity.enable()
        self._can_save = True


# VIEW ----------------------------------------------------------------------#

# Maps model symbols to their view counterparts
SYMBOL_MAP = {
    TANK_SYMBOL: TANK_DISPLAY,
    HEAL_SYMBOL: HEAL_DISPLAY,
    SCORPION_SYMBOL: SCORPION_DISPLAY,
    FIREFLY_SYMBOL: FIREFLY_DISPLAY,
}
SIDEBAR_COLS = 4


class BreachView:
    """
    Manages the view of a game of Into The Breach
    """
    def __init__(
        self,
        root: tk.Tk,
        board_dims: tuple[
            int, int
        ],
        save_callback: Optional[Callable[[], None]],
        load_callback: Optional[Callable[[], None]],
        turn_callback: Optional[Callable[[], None]],
    ) -> None:
        """
        Creates a view of a game of Into The Breach.

        Args:
            root (tk.Tk): root window
            board_dims (tuple[ int, int ]): initial board dimensions to display
            save_callback (Optional[Callable[[], None]]): Callback that should 
                                                          be called when the 
                                                          user clicks the 
                                                          "Save Game" button
            load_callback (Optional[Callable[[], None]]): Callback that should 
                                                          be called when the 
                                                          user clicks the 
                                                          "Load Game" button
            turn_callback (Optional[Callable[[], None]]): Callback that should 
                                                          be called when the 
                                                          user clicks the 
                                                          "End Turn" button
        """
        root.title(BANNER_TEXT)

        self._banner = tk.Label(
            root, text=BANNER_TEXT, font=BANNER_FONT
        )  # width and height arguments are different for Label, dont specify.
        self._game_frame = tk.Frame(root)
        self._grid = GameGrid(
            self._game_frame, board_dims, (GRID_SIZE, GRID_SIZE)
        )
        self._sidebar = SideBar(
            self._game_frame, (1, SIDEBAR_COLS), (SIDEBAR_WIDTH, GRID_SIZE)
        )
        self._control_bar = ControlBar(
            root,
            save_callback,
            load_callback,
            turn_callback,
            width=GRID_SIZE + SIDEBAR_WIDTH,
            height=CONTROL_BAR_HEIGHT,
        )

        self._banner.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)
        self._grid.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)
        self._sidebar.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)
        self._game_frame.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)
        self._control_bar.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)

    def bind_click_callback(self,
            click_callback: Callable[[tuple[int, int]], None]) -> None:
        """
        Binds a callback that will be called when the user clicks anywhere on 
        the board

        Args:
            click_callback (Callable[[tuple[int, int]], None]): Callback to be 
                                                                bound to the 
                                                                board display
        """
        self._grid.bind_click_callback(click_callback)

    def redraw(
        self,
        board: Board,
        entities: list[Entity],
        highlighted: Optional[list[tuple[int, int]]] = None,
        movement: bool = False,
    ) -> None:
        """
        Redraws the view based on the given board state and list of entities.

        Args:
            board (Board): The current board state
            entities (list[Entity]): The list of current entities
            highlighted (Optional[list[tuple[int, int]]]): List of tiles that 
                                                           should be 
                                                           highlighted. 
                                                           Optional: Defaults
                                                           None.
            movement (bool): True if highlight represents valid movement 
                             positions. False if highlight represents attack 
                             targets. Optional: Defaults to False.
        """
        self._grid.redraw(board, entities, highlighted, movement)
        self._sidebar.display(entities)


class GameGrid(AbstractGrid):
    """
    View component that displays board state for a game of Into The Breach.
    """
    def bind_click_callback(self, 
                    click_callback: Callable[[tuple[int, int]], None]) -> None:
        """
        Binds a callback that will be called when the user clicks anywhere on 
        the board

        Args:
            click_callback (Callable[[tuple[int, int]], None]): Callback to be 
                                                                bound to board
        """
        on_click = lambda e: click_callback(self.pixel_to_cell(e.x, e.y))
        self.bind("<Button-1>", on_click)
        self.bind("<Button-2>", on_click)  # NOTE: BIND BOTH FOR MACS

    def redraw(
        self,
        board: Board,
        entities: list[Entity],
        highlighted: Optional[list[tuple[int, int]]] = None,
        movement: bool = False,
    ) -> None:
        """
        Redraws the board based on the given board state and list of entities.

        Args:
            board (Board): The current board state
            entities (list[Entity]): The list of current entities
            highlighted (Optional[list[tuple[int, int]]]): List of tiles that 
                                                           should be 
                                                           highlighted. 
                                                           Optional: Defaults
                                                           None.
            movement (bool): True if highlight represents valid movement 
                             positions. False if highlight represents attack 
                             targets. Optional: Defaults to False.
        """
        self.clear()

        # See if move or attack highlight
        highlight_color = ATTACK_COLOR
        if movement:
            highlight_color = MOVE_COLOR

        # Display Board
        height, width = board.get_dimensions()
        self.set_dimensions((height, width))
        for row in range(height):
            for col in range(width):
                cell = (row, col)
                tile = board.get_tile(cell)
                if highlighted and cell in highlighted:
                    self.color_cell(cell, highlight_color)
                else:
                    # Color tile based on type
                    if tile.get_tile_name() == GROUND_NAME:
                        self.color_cell(cell, GROUND_COLOR)
                    elif tile.get_tile_name() == MOUNTAIN_NAME:
                        self.color_cell(cell, MOUNTAIN_COLOR)
                    elif tile.get_tile_name() == BUILDING_NAME:
                        building_color = BUILDING_COLOR
                        if tile.is_destroyed():
                            building_color = DESTROYED_COLOR
                        self.color_cell(cell, building_color)

                # Annotate buildings that are still standing
                if tile.get_tile_name() == BUILDING_NAME \
                        and not tile.is_destroyed():
                    self.annotate_position(cell, str(tile), ENTITY_FONT)

        # Display entities on top of board
        for entity in entities:
            symbol = SYMBOL_MAP[entity.get_symbol()]
            self.annotate_position(entity.get_position(), symbol, ENTITY_FONT)


class SideBar(AbstractGrid):
    """
    View component that displays the current state of entities for a game 
    of Into The Breach.
    """
    def __init__(
        self, 
        master: tk.Widget, 
        dimensions: tuple[int, int], 
        size: tuple[int, int]
    ) -> None:
        """
        Construct a new sidebar

        Args:
            master (tk.Widget): Widget that the sidebar should be packed into
            dimensions (tuple[int, int]): initial dimensions of sidebar table 
                                          to display
            size (tuple[int, int]): (width, height) dimensions of sidebar in 
                                    pixels
        """
        super().__init__(master, dimensions, size)

    def display(self, entities: list[Entity]) -> None:
        """
        Redraws the sidebar based on the provided list of entities. Entities
        will be displayed in priority order.

        Args:
            entities (list[Entity]): List of entities to display. Precondition:
                                     Entities appear in descending priority 
                                     order
        """
        self.clear()
        self.set_dimensions((len(entities) + 1, SIDEBAR_COLS))

        # Display headings
        for i, heading in enumerate(SIDEBAR_HEADINGS):
            self.annotate_position((0, i), heading, SIDEBAR_FONT)

        # Display entities
        for row, entity in enumerate(entities):
            for i, text in enumerate([
                    str(property) for property in [
                        SYMBOL_MAP[entity.get_symbol()],
                        entity.get_position(),
                        entity.get_health(),
                        entity.get_strength()
                    ]
            ]):
                self.annotate_position((row + 1, i), text, SIDEBAR_FONT)


class ControlBar(tk.Frame):
    """
    View element that contains buttons for the user to perform administrative
    actions.
    """
    def __init__(
        self,
        master: tk.Widget,
        save_callback: Optional[Callable[[], None]],
        load_callback: Optional[Callable[[], None]],
        turn_callback: Optional[Callable[[], None]],
        **kwargs,
    ) -> None:
        """
        Constructs a new control bar.

        Args:
            master (tk.Widget): Widget that the control bar should be packed 
                                into
            save_callback (Optional[Callable[[], None]]): Callback that should 
                                                          be called when the 
                                                          user clicks the 
                                                          "Save Game" button
            load_callback (Optional[Callable[[], None]]): Callback that should 
                                                          be called when the 
                                                          user clicks the 
                                                          "Load Game" button
            turn_callback (Optional[Callable[[], None]]): Callback that should 
                                                          be called when the 
                                                          user clicks the 
                                                          "End Turn" button
        """
        super().__init__(master, **kwargs)
        # NOTE, any reduction in this will be reasonably messy in itself
        self._save_button = tk.Button(self, 
                                      text=SAVE_TEXT, command=save_callback)
        self._load_button = tk.Button(self, 
                                      text=LOAD_TEXT, command=load_callback)
        self._turn_button = tk.Button(self, 
                                      text=TURN_TEXT, command=turn_callback)

        self._save_button.pack(side=tk.LEFT, expand=tk.TRUE)
        self._load_button.pack(side=tk.LEFT, expand=tk.TRUE)
        self._turn_button.pack(side=tk.LEFT, expand=tk.TRUE)


# CONTROLLER ----------------------------------------------------------------#
class IntoTheBreach:
    """
    Controller class that manages a game of Into The Breach
    """
    def __init__(self, root: tk.Tk, game_file: str) -> None:
        """
        Initialises a new game of Into the Breach

        Args:
            root (tk.Tk): Root window in which to display game
            game_file (str): file from which to load initial game state
        """
        self._root = root
        self._game_file = game_file
        self._model = None
        self.load_model(game_file)

        self._view = BreachView(
            root,
            self._model.get_board().get_dimensions(),
            save_callback=self._save_game,
            load_callback=self._load_game,
            turn_callback=self._end_turn,
        )
        self._view.bind_click_callback(self._handle_click)

        self._active_entity = None
        self.redraw()

    def redraw(self) -> None:
        """
        Redraws the game based on current game state
        """
        # Check if we are highlighting anything
        highlighted = None
        move = False
        if self._active_entity:
            if self._active_entity.is_friendly() \
                    and self._active_entity.is_active():
                highlighted = self._model.get_valid_movement_positions(
                    self._active_entity
                )
                move = True
            else:
                highlighted = self._active_entity.get_targets()

        self._view.redraw(
            self._model.get_board(), 
            self._model.get_entities(), 
            highlighted, 
            move
        )

    def set_focussed_entity(self, entity: Optional[Entity]) -> None:
        """
        Sets or clears the focussed entity

        Args:
            entity (Optional[Entity]): Entity to set as the focus, or None to 
                                       clear focussed entity
        """
        self._active_entity = entity

    def make_move(self, position: tuple[int, int]) -> None:
        """
        Attempts to move the focussed entity to a specified position, doing so 
        only if this is a legal move.

        Args:
            position (tuple[int, int]): Position to move focussed entity to.
        """
        if self._active_entity:
            self._model.attempt_move(self._active_entity, position)
            self.set_focussed_entity(None)
            self.redraw()

    def load_model(self, file_path: str) -> None:
        """
        Replaces current game state with the game state provided in the 
        specified file.

        Args:
            file_path (str): file from which to load new game state.
        """
        # NOTE: this is just one solution. There are many ways to parse this
        try:
            with open(file_path) as f:
                # Read in board state
                text_board = []
                row = f.readline().rstrip() # NOTE assuming at least one row
                while row:  # Blank lines between board and entities
                    text_row = []
                    for tile in row:
                        text_row.append(tile)
                    text_board.append(text_row)
                    row = f.readline().rstrip()

                # Read in entities (Ordered as they appear in file)
                entity_text = f.read().splitlines() # remaining lines in file
                entities = []
                for entity_string in entity_text:
                    entity_values = entity_string.split(",")
                    entities.append(
                        ENTITY_MAP[entity_values[0]](
                            (int(entity_values[1]), int(entity_values[2])),
                            *map(int, entity_values[3:]),
                        )
                    ) 

            self._model = BreachModel(Board(text_board), entities)

        except IOError as e:
            messagebox.showerror(IO_ERROR_TITLE, 
                                 IO_ERROR_MESSAGE + str(e))

    def _save_game(self) -> None:
        """
        Saves the current game state to a user specified file if it is valid to 
        do so
        """
        # Check if in valid state to save
        if self._model.ready_to_save():
            file_path = filedialog.asksaveasfilename()
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(str(self._model))
        else:
            messagebox.showerror(INVALID_SAVE_TITLE, INVALID_SAVE_MESSAGE)

    def _load_game(self) -> None:
        """
        Loads a new game from a user defined file.
        """
        self.set_focussed_entity(None)
        file_path = filedialog.askopenfilename()
        if file_path:
            self._game_file = file_path
            self.load_model(file_path)

        self.redraw()

    def _end_turn(self) -> None:
        """
        Advances the game to the next turn, and handles asking the user 
        if they want to play again if they win or lose.
        """
        self.set_focussed_entity(None)
        self._model.end_turn()
        self.redraw()

        # Check for termination
        result = None
        if self._model.has_lost():
            result = "Lost"
        elif self._model.has_won():
            result = "Win"
        if result:
            message = f"You {result}!"
            if messagebox.askyesno(message, message + " " + PLAY_AGAIN_TEXT):
                self.load_model(self._game_file)
                self.redraw()
            else:
                self._root.destroy()

    def _handle_click(self, position: tuple[int, int]) -> None:
        """
        Sets the focussed entity if the given position contains an entity.
        Otherwise attempts to move the focussed entity to the given position.

        Args:
            position (tuple[int, int]): position clicked by the user.
        """
        entities = self._model.entity_positions()
        if position in entities:
            self._active_entity = entities[position]
            self.redraw()
        else:
            self.make_move(position)

def play_game(root: tk.Tk, file_path: str) -> None:
    """
    Plays the game.

    Args:
        file_path: The path to file containing level.
    """
    app = IntoTheBreach(root, file_path)
    root.mainloop()


def main() -> None:
    """The main function."""
    root = tk.Tk()
    play_game(root, "levels/level1.txt")


if __name__ == "__main__":
    main()
