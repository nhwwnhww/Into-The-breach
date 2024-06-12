# DO NOT modify or add any import statements
from a2_support import *
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional, Callable


# Name: Wei Weng
# Student Number: 47981739 
# ----------------


# Write your classes and functions here

class Tile():
    """
    Tile is an abstract class that provides default behavior for tiles in the game. 
    All instantiated types of tiles inherit from this class.
    Tiles are represented by the character 'T'. This class can be inherited or overridden by specific types of tiles.
    """
    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the tile.
        
        Returns:
            str: A string representation of the tile instance.
        """
        return f"{TILE_NAME}()"
    
    def __str__(self) -> str:
        """
        Returns the character representing the type of the tile.
        
        Returns:
            str: The character symbol of the tile.
        """
        return TILE_SYMBOL
    def get_tile_name(self) -> str:
        """
        Returns the name of the type of the tile, which is the name of the most specific class to which the tile belongs.
        
        Returns:
            str: The name of the tile type.
        """
        return TILE_NAME
    
    def is_blocking(self) -> bool:
        """
        Returns True only when the tile is blocking. By default, tiles are not blocking.
        
        Returns:
            bool: False, indicating the tile is not blocking by default.
        """
        return False

class Ground(Tile):
    """
    Ground is a class that inherits from Tile. It represents simple, walkable ground with no special properties.
    Ground tiles are never blocking and are represented by GROUND_SYMBOL(' ').
    """
    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the ground tile.
        
        Returns:
            str: A string representation of the ground tile instance.
        """
        return f"{GROUND_NAME}()"
    
    def __str__(self) -> str:
        """
        Returns the character representing the ground tile, which is a space character.
        
        Returns:
            str: The character symbol of the ground tile.
        """
        return GROUND_SYMBOL
    
    def get_tile_name(self) -> str:
        """
        Returns the name of the tile type, which is 'Ground'.
        
        Returns:
            str: The name of the tile type.
        """
        return GROUND_NAME
      
class Mountain(Tile):
    """
    Mountain is a class that inherits from Tile. It represents unpassable terrain.
    Mountain tiles are always blocking and are represented by the character 'M'.
    """
    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the mountain tile.
        
        Returns:
            str: A string representation of the mountain tile instance.
        """
        return f"{MOUNTAIN_NAME}()"
    
    def __str__(self) -> str:
        """
        Returns the character representing the mountain tile, which is 'M'.
        
        Returns:
            str: The character symbol of the mountain tile.
        """
        return MOUNTAIN_SYMBOL
    
    def get_tile_name(self) -> str:
        """
        Returns the name of the tile type, which is 'Mountain'.
        
        Returns:
            str: The name of the tile type.
        """
        return MOUNTAIN_NAME
    
    def is_blocking(self) -> bool:
        """
        Returns True, indicating the mountain tile is blocking.
        
        Returns:
            bool: True, indicating the tile is blocking.
        """
        return True
    
class Building(Tile):
    """
    Building is a class that inherits from Tile. Building tiles represent one or more buildings that the player must protect from enemies.
    Building tiles have an integer health value and can be destroyed. A building tile is destroyed when its health drops to zero.
    The health value of a building can never increase above 9. Building tiles are blocking only when they are not destroyed.
    Building tiles are represented by their current health value, as a string.
    """
    def __init__(self, initial_health: int) -> None:
        """
        Initializes a building with the specified health. The health value is clamped between 0 and MAX_BUILDING_HEALTH(9) inclusive.
        
        Args:
            initial_health (int): The initial health of the building, expected to be between 0 and MAX_BUILDING_HEALTH(9) inclusive.
        """
        # get the valid initial health (between 0 to MAX_BUILDING_HEALTH)
        self._health = max(0,min(initial_health, MAX_BUILDING_HEALTH))

    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the building tile.
        
        Returns:
            str: A string representation of the building tile instance.
        """
        return f"{BUILDING_NAME}({self._health})"

    def __str__(self) -> str:
        """
        Returns the character representing the building tile, which is its current health value as a string.
        
        Returns:
            str: The current health value of the building tile as a string.
        """
        return str(self._health)
    
    def get_tile_name(self) -> str:
        """
        Returns the name of the tile type, which is 'Building'.
        
        Returns:
            str: The name of the tile type.
        """
        return BUILDING_NAME

    def is_destroyed(self) -> bool:
        """
        Returns True only when the building is destroyed (health <= 0).
        
        Returns:
            bool: True if the building is destroyed, False otherwise.
        """
        return self._health <= 0
    
    def is_blocking(self) -> bool:
        """
        Returns True if the building tile is not destroyed (health > 0), otherwise False.
        
        Returns:
            bool: True if the tile is blocking, False otherwise.
        """
        # if the bilding is destroyed then it is not blocking
        return not self.is_destroyed()

    def damage(self, damage:int) -> None:
        """
        Reduces the health of the building by the amount specified. 
        The health of the building is capped between 0 and 9 inclusive.
        This function does nothing if the building is already destroyed.
        
        Args:
            damage (int): The amount of damage to apply to the building. 
                          Can be negative to indicate healing, but health is capped at MAX_BUILDING_HEALTH(9).
        """
        if not self.is_destroyed():
            # get the valid initial health (between 0 to MAX_BUILDING_HEALTH)
            self._health = max(0, min(self._health - damage, MAX_BUILDING_HEALTH))

class Board():
    """
    Board represents a structured set of tiles. A board organizes tiles in a rectangular grid, where each
    tile has an associated (row, column) position. (0,0) represents the top-left corner, (1,0) represents
    the position directly below the top-left corner, and (0, 1) represents the position directly right of the
    top left corner.
    """
    def __init__(self, board: list[list[str]]) -> None:
        """
        Initializes a new Board instance from the information in the board argument.
        
        Args:
            board (list[list[str]]): A 2D list representing rows and columns of the board. Each character 
                                     in the inner lists represents a tile type.
        
        Preconditions:
            - Each list (each row) within the given board will have the same length.
            - The given array will contain at least one row.
            - Each character provided will be the string representation of one of the tile subclasses.
        """
        self._board = []
        for board_rows in board:
            row = []
            for symbol in board_rows:
                if symbol == GROUND_SYMBOL:
                    row.append(Ground())
                elif symbol == MOUNTAIN_SYMBOL:
                    row.append(Mountain())
                elif symbol.isdigit():
                    row.append(Building(int(symbol)))
            self._board.append(row)

    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the board.
        
        Returns:
            str: A string representation of the board instance.
        """
        repr_board = []
        for row in self._board:
            row_repr = []
            for symbol in row:
                if isinstance(symbol, Ground):
                    row_repr.append(GROUND_SYMBOL)
                elif isinstance(symbol, Mountain):
                    row_repr.append(MOUNTAIN_SYMBOL)
                elif isinstance(symbol, Building):
                    row_repr.append(str(symbol))
            repr_board.append(row_repr)
        return f"Board({repr_board})"
    
    def __str__(self) -> str:
        """
        Returns a string representation of the board. This is the string formed by concatenating the
        characters representing each tile of a row in the order they appear (left to right), and then
        concatenating each row in order (from top to bottom), separating each row with a new line character.
        
        Returns:
            str: A string representation of the board for display.
        """
        str_board = []
        for row in self._board:
            row_str = []
            for symbol in row:
                if isinstance(symbol,Mountain):
                    row_str.append(MOUNTAIN_SYMBOL)
                elif isinstance(symbol,Building):
                    row_str.append(str(symbol))
                else:
                    row_str.append(GROUND_SYMBOL)
            str_board.append("".join(row_str))
        return "\n".join(str_board)

    def get_dimensions(self) -> tuple[int, int]:
        """
        Returns the dimensions of the board.
        
        Returns:
            tuple[int, int]: A tuple containing the number of rows and columns on the board.
        """
        return (len(self._board), len(self._board[0]))
    
    def get_tile(self, position:tuple[int,int]) -> Tile:
        """
        Returns the Tile instance located at the given position.
        
        Args:
            position (tuple[int, int]): The position (row, column) of the tile.
        
        Returns:
            Tile: The tile object at the given position.
        
        Preconditions:
            The provided position will not be out of bounds.
        """
        row,col = position
        return self._board[row][col]
    
    def get_buildings(self) -> dict[tuple[int, int], Building]:
        """
        Returns a dictionary mapping the positions of buildings to the building instances at those positions.
        This dictionary should only contain positions at which there is a building tile.
        
        Returns:
            dict[tuple[int, int], Building]: A dictionary with positions as keys and Building instances as values.
        """
        building = {}
        for i, row in enumerate(self._board):
            for j, tile in enumerate(row):
                if isinstance(tile, Building):
                    building[(i,j)] = tile
        return building

class Entity():
    """
    Entity is an abstract class from which all instantiated types of entity inherit. This class provides
    default entity behavior, which can be inherited or overridden by specific types of entities.
    """
    def __init__(self,
        position: tuple[int, int],
        initial_health: int,
        speed: int,
        strength: int) -> None:
        """
        Initializes a new entity with the specified position, health, speed, and strength.
        
        Args:
            position (tuple[int, int]): The (row, column) position of the entity.
            initial_health (int): The initial health of the entity.
            speed (int): The speed of the entity.
            strength (int): The strength of the entity.
        """
        self._position = position
        self._health = max(0,initial_health)
        self._speed = speed
        self._strength = strength
        
    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the entity.
        
        Returns:
            str: A string representation of the entity instance.
        """
        return f"{ENTITY_NAME}({self._position}, {self._health}, {self._speed}, {self._strength})"
    
    def __str__(self) -> str:
        """
        Returns the string representation of the entity.
        
        Returns:
            str: A string representation of the entity.
        """
        x,y = self._position
        return f"{ENTITY_SYMBOL},{x},{y},{self._health},{self._speed},{self._strength}"
    
    def get_symbol(self) -> str:
        """
        Returns the character that represents the entity type.
        
        Returns:
            str: The character representing the entity type.
        """
        return ENTITY_SYMBOL

    def get_name(self) -> str:
        """
        Returns the name of the type of the entity.
        
        Returns:
            str: The name of the type of the entity.
        """
        return ENTITY_NAME

    def get_position(self) -> tuple[int, int]:
        """
        Returns the current position of the entity.
        
        Returns:
            tuple[int, int]: The (row, column) position of the entity.
        """
        return self._position

    def set_position(self, position: tuple[int, int]) -> None:
        """
        Moves the entity to the specified position.
        
        Args:
            position (tuple[int, int]): The new (row, column) position of the entity.
        """
        self._position = position

    def get_health(self) -> int:
        """
        Returns the current health of the entity.
        
        Returns:
            int: The current health of the entity.
        """
        return self._health

    def get_speed(self) -> int:
        """
        Returns the speed of the entity.
        
        Returns:
            int: The speed of the entity.
        """
        return self._speed

    def get_strength(self) -> int:
        """
        Returns the strength of the entity.
        
        Returns:
            int: The strength of the entity.
        """
        return self._strength

    def damage(self, damage: int) -> None:
        """
        Reduces the health of the entity by the specified amount.
        
        Args:
            damage (int): The amount of damage to be applied to the entity's health.
        """
        if self.is_alive():  
            self._health = max(0,(self._health-damage))

    def is_alive(self) -> bool:
        """
        Returns True if and only if the entity is not destroyed.
        
        Returns:
            bool: True if the entity is alive, False otherwise.
        """
        return self._health > 0

    def is_friendly(self) -> bool:
        """
        Returns True if and only if the entity is friendly.
        By default, entities are not friendly
        
        Returns:
            bool: True if the entity is friendly, False otherwise.
        """
        return False

    def get_targets(self) -> list[tuple[int, int]]:
        """
        Returns the positions that would be attacked by the entity during a combat phase.
        
        Returns:
            list[tuple[int, int]]: A list of positions that would be attacked by the entity.
        """
        row,col = self.get_position()
        targets = [(row + dr, col + dc) for dr, dc in PLUS_OFFSETS]
        return targets

    def attack(self, entity: "Entity") -> None:
        """
        Applies this entity’s effect to the given entity.
        
        Args:
            entity (Entity): The entity to be attacked.
        """

        entity.damage(self._strength)
        pass

class Mech(Entity):
    """
    Mech is an abstract class that inherits from Entity from which all instantiated types of mech inherit.
    This class provides default mech behavior, which can be inherited or overridden by specific types of mechs.
    """
    def __init__(self, position: tuple[int, int], initial_health: int, speed: int, strength: int) -> None:
        """
        Initializes a new mech with the specified position, health, speed, and strength.
        
        Args:
            position (tuple[int, int]): The (row, column) position of the mech.
            initial_health (int): The initial health of the mech.
            speed (int): The speed of the mech.
            strength (int): The strength of the mech.
        """
        super().__init__(position, initial_health, speed, strength)
        self._active = True

    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the mech.
        
        Returns:
            str: A string representation of the mech instance.
        """
        return f"{MECH_NAME}({self._position}, {self._health}, {self._speed}, {self._strength})"
    
    def __str__(self) -> str:
        """
        Returns the string representation of the mech.
        
        Returns:
            str: A string representation of the mech.
        """
        x,y = self._position
        return f"{MECH_SYMBOL},{x},{y},{self._health},{self._speed},{self._strength}"

    def get_symbol(self) -> str:
        """
        Returns the character that represents the mech type.
        
        Returns:
            str: The character representing the mech type.
        """
        return MECH_SYMBOL
    
    def get_name(self) -> str:
        """
        Returns the name of the type of the mech.
        
        Returns:
            str: The name of the type of the mech.
        """
        return MECH_NAME
    
    def is_friendly(self) -> bool:
        """
        Returns True since mechs are always friendly.
        
        Returns:
            bool: True, mechs are always friendly.
        """
        return True

    def enable(self) -> None:
        """
        Sets the mech to be active.
        """
        self._active = True
        pass

    def disable(self) -> None:
        """
        Sets the mech to not be active.
        """
        self._active = False
        pass

    def is_active(self) -> bool:
        """
        Returns True if the mech is active, False otherwise.
        
        Returns:
            bool: True if the mech is active, False otherwise.
        """
        return self._active

class TankMech(Mech):
    """
    TankMech inherits from Mech. TankMech represents a type of mech that attacks at a long range
    horizontally. Tank mechs are represented by the character T.
    """
    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the tank mech.
        
        Returns:
            str: A string representation of the tank mech instance.
        """
        return f"{TANK_NAME}({self._position}, {self._health}, {self._speed}, {self._strength})"
    
    def __str__(self) -> str:
        """
        Returns the string representation of the tank mech.
        
        Returns:
            str: A string representation of the tank mech.
        """
        x,y = self._position
        return f"{TANK_SYMBOL},{x},{y},{self._health},{self._speed},{self._strength}"
    
    def get_symbol(self) -> str:
        """
        Returns the character that represents the tank mech type.
        
        Returns:
            str: The character representing the tank mech type.
        """
        return TANK_SYMBOL
    
    def get_name(self) -> str:
        """
        Returns the name of the type of the tank mech.
        
        Returns:
            str: The name of the type of the tank mech.
        """
        return TANK_NAME
    
    def get_targets(self) -> list[tuple[int, int]]:
        """
        Returns the positions that would be attacked by the tank mech during a combat phase.
        
        Returns:
            list[tuple[int, int]]: A list of positions that would be attacked by the tank mech.
        """
        row,col = self.get_position()
        targets = []
        for i in range(-TANK_RANGE, TANK_RANGE + 1):
            if i != 0:
                targets.append((row, col + i))
        return targets

class HealMech(Mech):
    """
    HealMech inherits from Mech. HealMech represents a type of mech that does not deal damage, but
    instead supports friendly units and buildings by healing (that is, increasing health); that is, HealMech
    objects ‘damage‘ friendly units and buildings by a negative amount. In order to achieve this, the
    get_strength method of the HealMech should return a value equal to the negative of the heal mech’s
    strength. A heal mech does nothing when attacking an entity that is not friendly. Heal mechs are
    represented by the character H.
    """
    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the heal mech.
        
        Returns:
            str: A string representation of the heal mech instance.
        """
        return f"{HEAL_NAME}({self._position}, {self._health}, {self._speed}, {self._strength})"
    
    def __str__(self) -> str:
        """
        Returns the string representation of the heal mech.
        
        Returns:
            str: A string representation of the heal mech.
        """
        x,y = self._position
        return f"{HEAL_SYMBOL},{x},{y},{self._health},{self._speed},{self._strength}"
    
    def get_symbol(self) -> str:
        """
        Returns the character that represents the heal mech type.
        
        Returns:
            str: The character representing the heal mech type.
        """
        return HEAL_SYMBOL
    
    def get_name(self) -> str:
        """
        Returns the name of the type of the heal mech.
        
        Returns:
            str: The name of the type of the heal mech.
        """
        return HEAL_NAME
    
    def get_strength(self) -> int:
        """
        Returns the strength of the heal mech.
        
        Returns:
            int: The strength of the heal mech.
        """
        return -self._strength
    
    def attack(self, entity: Entity) -> None:
        """
        Applies the heal mech's effect to the given entity.
        
        Args:
            entity (Entity): The entity(Only for Mech) to apply the heal mech's effect to.
        """
        if isinstance(entity, Mech):
            entity.damage(-self._strength)

class Enemy(Entity):
    """
    Enemy is an abstract class that inherits from Entity from which all instantiated types of enemy
    inherit. This class provides default enemy behavior, which can be inherited or overridden by specific
    types of enemies. All enemies have an objective, which is a position that the entity wants to move
    towards. The objective of all enemies upon instantiation is the enemy’s current position. Enemies
    of any type are never friendly. Abstract enemies are represented by the character N.
    """
    def __init__(self, position: tuple[int, int], initial_health: int, speed: int, strength: int) -> None:
        """
        Initializes a new Enemy instance.

        Args:
            position (tuple[int, int]): The initial position of the enemy.
            initial_health (int): The initial health of the enemy.
            speed (int): The speed of the enemy.
            strength (int): The strength of the enemy.
        """
        super().__init__(position, initial_health, speed, strength)
        self._objective = position

    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the enemy.
        
        Returns:
            str: A string representation of the enemy instance.
        """
        return f"{ENEMY_NAME}({self._position}, {self._health}, {self._speed}, {self._strength})"
    
    def __str__(self) -> str:
        """
        Returns the string representation of the enemy.
        
        Returns:
            str: A string representation of the enemy.
        """
        x,y = self._position
        return f"{ENEMY_SYMBOL},{x},{y},{self._health},{self._speed},{self._strength}"
    
    def get_symbol(self) -> str:
        """
        Returns the character that represents the enemy type.
        
        Returns:
            str: The character representing the enemy type.
        """
        return ENEMY_SYMBOL
    
    def get_name(self) -> str:
        """
        Returns the name of the type of the enemy.
        
        Returns:
            str: The name of the type of the enemy.
        """
        return ENEMY_NAME

    def get_objective(self) -> tuple[int, int]:
        """
        Returns the current objective of the enemy.
        
        Returns:
            tuple[int, int]: The (row, column) position that the enemy wants to move towards.
        """
        return self._objective

    def update_objective(self, 
                         entities: list[Entity], 
                         buildings: dict[tuple[int, int],
                         Building]) -> None:
        """
        Updates the objective of the enemy based on a list of entities and dictionary of buildings.
        
        Args:
            entities (list[Entity]): A list of entities sorted in descending priority order.
            buildings (dict[tuple[int, int], Building]): A dictionary mapping positions to building instances.
        """
        if self.get_symbol() == SCORPION_SYMBOL:
            highest_health_mech = None
            highest_health = -1
            for entity in entities:
                if entity.is_friendly() and entity.get_health() > highest_health:
                    highest_health = entity.get_health()
                    highest_health_mech = entity
            if highest_health_mech:
                self._objective = highest_health_mech.get_position()
        elif self.get_symbol() == FIREFLY_SYMBOL:
            target_position = None
            lowest_health = MAX_BUILDING_HEALTH
            for position, building in buildings.items():
                if building._health < lowest_health:
                    lowest_health = building._health
                    target_position = position
            if target_position:
                self._objective = target_position
            else:
                self._objective = None
        else:
            self._objective = self.get_position()

class Scorpion(Enemy):
    """
    Scorpion inherits from Enemy. Scorpion represents a type of enemy that attacks at a moderate
    range in all directions, and targets mechs with the highest health. Scorpions are represented by the
    character S.
    """

    def __init__(self, position: tuple[int, int], initial_health: int, speed: int, strength: int) -> None:
        """
        Initializes a new Scorpion instance.

        Args:
            position (tuple[int, int]): The initial position of the Scorpion.
            initial_health (int): The initial health of the Scorpion.
            speed (int): The speed of the Scorpion.
            strength (int): The strength of the Scorpion.
        """
        super().__init__(position, initial_health, speed, strength)

    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the Scorpion.
        
        Returns:
            str: A string representation of the Scorpion instance.
        """
        return f"{SCORPION_NAME}({self._position}, {self._health}, {self._speed}, {self._strength})"
    
    def __str__(self) -> str:
        """
        Returns the string representation of the Scorpion.
        
        Returns:
            str: A string representation of the Scorpion.
        """
        x, y = self._position
        return f"{SCORPION_SYMBOL},{x},{y},{self._health},{self._speed},{self._strength}"

    def get_symbol(self) -> str:
        """
        Returns the character that represents the Scorpion type.
        
        Returns:
            str: The character representing the Scorpion type.
        """
        return SCORPION_SYMBOL
    
    def get_name(self) -> str:
        """
        Returns the name of the type of the Scorpion.
        
        Returns:
            str: The name of the type of the Scorpion.
        """
        return SCORPION_NAME
    
    def get_targets(self) -> list[tuple[int, int]]:
        """
        Returns the positions that would be attacked by the Scorpion during a combat phase.

        Returns:
            list[tuple[int, int]]: A list of positions that would be attacked by the Scorpion.
        """
        row, col = self.get_position()
        targets = []
        for i in range(-SCORPION_RANGE, SCORPION_RANGE + 1):
            if i != 0:
                targets.append((row + i, col))
                targets.append((row, col + i))
        return targets
    
class Firefly(Enemy):
    """
    Firefly inherits from Enemy. Firefly represents a type of enemy that attacks at a long range
    vertically, and targets buildings with the lowest health. Fireflies are represented by the character F.
    """

    def __init__(self, position: tuple[int, int], initial_health: int, speed: int, strength: int) -> None:
        """
        Initializes a new Firefly instance.

        Args:
            position (tuple[int, int]): The initial position of the Firefly.
            initial_health (int): The initial health of the Firefly.
            speed (int): The speed of the Firefly.
            strength (int): The strength of the Firefly.
        """
        super().__init__(position, initial_health, speed, strength)

    def __repr__(self) -> str:
        """
        Returns a machine-readable string that could be used to construct an identical instance of the Firefly.
        
        Returns:
            str: A string representation of the Firefly instance.
        """
        return f"{FIREFLY_NAME}({self._position}, {self._health}, {self._speed}, {self._strength})"
    
    def __str__(self) -> str:
        """
        Returns the string representation of the Firefly.
        
        Returns:
            str: A string representation of the Firefly.
        """
        x, y = self._position
        return f"{FIREFLY_SYMBOL},{x},{y},{self._health},{self._speed},{self._strength}"

    def get_symbol(self) -> str:
        """
        Returns the character that represents the Firefly type.
        
        Returns:
            str: The character representing the Firefly type.
        """
        return FIREFLY_SYMBOL
    
    def get_name(self) -> str:
        """
        Returns the name of the type of the Firefly.
        
        Returns:
            str: The name of the type of the Firefly.
        """
        return FIREFLY_NAME  
    
    def get_targets(self) -> list[tuple[int, int]]:
        """
        Returns the positions that would be attacked by the Firefly during a combat phase.

        Returns:
            list[tuple[int, int]]: A list of positions that would be attacked by the Firefly.
        """
        row, col = self.get_position()
        targets = []
        for i in range(-FIREFLY_RANGE, FIREFLY_RANGE + 1):
            if i != 0:
                targets.append((row + i, col))
        return targets

class BreachModel():
    def __init__(self, board: Board, entities: list[Entity]) -> None:
        """
        Instantiates a new model class with the given board and entities.

        Precondition:
            The provided list of entities is in descending priority order,
            with the highest priority entity being the first element of the list,
            and the lowest priority entity being the last element of the list.

        Parameters:
            board (Board): The game board.
            entities (list[Entity]): The list of entities.
        """
        # Initialize model with board and entities
        self._board = board
        self._entities = entities
        self._move_made = False
        pass
    
    def __str__(self) -> str:
        """
        Returns the string representation of the model.

        The string representation of a model is the string representation of the game board,
        followed by a blank line, followed by the string representation of all game entities
        in descending priority order, separated by newline characters.

        Returns:
            str: The string representation of the model.
        """
        entities_str = "\n".join(str(entity) for entity in self._entities)
        string = str(self._board) + '\n\n' + entities_str
        return string
    
    def get_board(self) -> Board:
        """
        Returns the current board instance.

        Returns:
            Board: The current board instance.
        """
        return self._board
    
    def get_entities(self) -> list[Entity]:
        """
        Returns the list of all entities in descending priority order.

        Returns:
            list[Entity]: The list of all entities.
        """
        return self._entities
    
    def has_won(self) -> bool:
        """
        Check if the player has won the game.
        The player wins if all enemies are destroyed, at least one mech is not destroyed, 
        and at least one building is not destroyed.

        """
        mech_list = [entity for entity in self._entities if isinstance(entity, Mech)]
        enemy_list = [entity for entity in self._entities if isinstance(entity, Enemy)]
        if (any(entity.is_alive() for entity in mech_list) and 
            any(not building.is_destroyed() for position, building in self._board.get_buildings().items())):
            return all(not entity.is_alive() for entity in enemy_list)
        return False
    
    def has_lost(self) -> bool:
        """
        # Check if the game is in a loss state:
        all buildings on the board are destroyed
        or 
        all mechs are destroyed.
        """
        mech_list = [entity for entity in self._entities if isinstance(entity, Mech)]
        return all(building.is_destroyed() for position, building in self._board.get_buildings().items()) or all(not entity.is_alive() for entity in mech_list)
    
    def entity_positions(self) -> dict[tuple[int, int], Entity]:
        """
        Returns a dictionary containing all entities, indexed by entity position.

        Returns:
            dict[tuple[int, int], Entity]: A dictionary containing all entities indexed by entity position.
        """
        # Return a dictionary containing all entities indexed by entity position
        entity_positions_dict = {entity.get_position(): entity for entity in self._entities}
        return entity_positions_dict
    
    def get_valid_movement_positions(self, entity: Entity) -> list[tuple[int, int]]:
        """
        Returns the list of positions that the given entity could move to during the relevant movement phase.
        Note that this function does not check if the entity has already moved during a given movement phase.
        The list is ordered such that positions in higher rows appear before positions in lower rows.
        Within the same row, positions in columns further left appear before positions in columns further right.
        
        Args:
            entity (Entity): The entity for which to find valid movement positions.

        Returns:
            list[tuple[int, int]]: A list of valid movement positions.
        """
        # Return the list of valid movement positions for the given entity
        valid_positions = []
        # Initialise
        max_speed = entity.get_speed()
        current_position = entity.get_position()
        dimensions = self._board.get_dimensions()
        
        # searching the board
        for i in range(dimensions[0]):
            for j in range(dimensions[1]):
                search_position = (i,j)

                if 0 <= i < dimensions[0] and 0 <= j < dimensions[1]:
                    #get the distance between entity current postion and search postion
                    distance = get_distance(self, current_position, search_position)

                    if 0 <= distance <= max_speed:
                        tile = self._board.get_tile(search_position)

                        if tile is not None and not tile.is_blocking() and \
                        current_position != search_position:
                            valid_positions.append(search_position)
            
        """
        The list should be ordered such that positions in higher rows appear
        before positions in lower rows. Within the same row, positions in columns further left should
        appear before positions in columns further right

        key = lambda pos: (pos[0], pos[1])
        pos[0] -> making higher row coordinates come first (which is the low index)
        pos[1] -> the order remains normal
        """
        valid_positions.sort(key = lambda pos: (-pos[0], pos[1]))
        return valid_positions
    
    def attempt_move(self, entity: Entity, position: tuple[int, int]) -> None:
        """
        Moves the given entity to the specified position only if the entity is friendly, active, and can
        move to that position according to the game rules. Disables entity if a successful move is made.

        Args:
            entity (Entity): The entity to move.
            position (tuple[int, int]): The position to move the entity to.
        """
        # Check if the entity is friendly and active
        if isinstance(entity,Mech) and entity.is_active():
            if position in self.get_valid_movement_positions(entity):
                # Update the position of the entity
                entity.set_position(position)
                # Disable the entity after successful move
                entity.disable()
                self._move_made = True
            
    def ready_to_save(self) -> bool:
        """
        Returns True only when no move has been made since the last call to end turn.

        Returns:
            bool: True if no move has been made since the last call to end turn, False otherwise.
        """
        # Check if no move has been made since the last call to end turn
        return not self._move_made
    
    def assign_objectives(self) -> None:
        """
        Updates the objectives of all enemies based on the current game state.

        This method iterates through all entities and updates the objective for each enemy based on
        the current game state, considering the positions of entities and buildings.

        """
        # Update the objectives of all enemies based on the current game state
        for entity in self.get_entities():
            # if not entity.is_friendly():
            if isinstance(entity,Enemy):
                entity.update_objective(self._entities,self._board.get_buildings())
    
    def move_enemies(self) -> None:
        """
        Moves each enemy to the valid movement position that minimizes the distance of the shortest
        valid path between the position and the enemy’s objective.
        """

        # Update the objectives of all enemies based on the current game state
        self.assign_objectives()
        # Get the enemy in descending priority order
        entities = [entity for entity in self.get_entities() if isinstance(entity, Enemy)]

        for enemy in entities:
            # Get valid movement positions for the enemy
            valid_positions = self.get_valid_movement_positions(enemy)
            if valid_positions and enemy._objective:
                # Calculate distances to objective for each valid position
                distances = {}
                for position in valid_positions:
                    if get_distance(self,enemy.get_objective(), position) > 0:
                        distances[position] = get_distance(self,enemy.get_objective(), position)
                if distances:
                    # Find the position with the shortest distance to the objective
                    min_distance_position = min(distances, key=distances.get)
                    
                    # Move enemy to the position with the shortest valid path
                    enemy.set_position(min_distance_position)
    
    def make_attack(self, entity: Entity) -> None:
        """
        Makes the given entity perform an attack against every tile that is currently a target of the entity.
        """
        # Iterate over all targeted tiles
        for target_pos in entity.get_targets():
            dimensions = self._board.get_dimensions()
            if 0 <= target_pos[0] < dimensions[0] and 0 <= target_pos[1] < dimensions[1]:
                # Apply effects based on the type of tile
                building = self._board.get_buildings()
                if target_pos in building:
                    target_building = self._board.get_tile(target_pos)
                    # If the tile is a building, reduce its health by the strength of the attacking entity
                    x,y = target_pos
                    target_building.damage(entity.get_strength())
                    self._board._board[x][y] = Building(target_building._health)
                if target_pos in self.entity_positions():

                    target = self.entity_positions()[target_pos]

                    if isinstance(entity, HealMech):
                        if isinstance(target,Mech):
                            target.damage(entity.get_strength())
                            
                    else:
                        if isinstance(target, Entity):
                            # If the attacking entity is an enemy, destroy the entity with lower priority
                            entity.attack(target)
                            if not target.is_alive():
                                # If the enemy entity is destroyed, remove it from the board
                                self._entities.remove(target)
    
    def end_turn(self) -> None:
        """Executes the attack and enemy movement phases and sets all mechs to be active."""
        for entity in self._entities:
            self.make_attack(entity)
            if isinstance(entity, Mech):
                entity.enable()
        self.move_enemies()
        self._move_made = False
        
class GameGrid(AbstractGrid):
    """
    GameGrid inherits from AbstractGrid provided in a2 support.py. GameGrid is a view component
    that displays the game board, with entities overlaid on top. Tiles are represented by certain colored
    squares, and entities are displayed by annotating special Unicode symbols (that is, regular plaintext
    that does not appear on most keyboards) on top of these squares. a2 support.py provides the exact
    colors and unicode symbols for display.
    """
    def redraw(self, 
               board: Board, 
               entities: list[Entity], 
               highlighted: list[tuple[int, int]] = None, 
               movement: bool = False) -> None:
        """
        Redraws the game grid based on the current board state, entities, and any highlighted positions.

        Args:
            board (Board): The current game board.
            entities (list[Entity]): A list of all entities on the board.
            highlighted (list[tuple[int, int]], optional): Positions to be highlighted. Defaults to None.
            movement (bool, optional): If True, use movement color for highlighting; otherwise, use attack color. Defaults to False.
        """
        self.clear()

        dimensions = board.get_dimensions()
        self.set_dimensions(dimensions)

        if highlighted:
            self.highlight_cells(highlighted, movement)

        self.draw_tiles(board, dimensions, highlighted)
        self.annotate_buildings(board, dimensions)
        self.annotate_entities(entities)

    def highlight_cells(self, highlighted: list[tuple[int, int]], movement: bool) -> None:
        """
        Highlights the specified cells on the grid.

        Args:
            highlighted (list[tuple[int, int]]): Positions to be highlighted.
            movement (bool): If True, use movement color for highlighting; otherwise, use attack color.
        """
        colour = MOVE_COLOR if movement else ATTACK_COLOR
        for position in highlighted:
            self.color_cell(position, colour)

    def draw_tiles(self, board: Board, dimensions: tuple[int, int], highlighted: list[tuple[int, int]] = None) -> None:
        """
        Draws the tiles on the board with appropriate colors.

        Args:
            board (Board): The current game board.
            dimensions (tuple[int, int]): The dimensions of the board.
            highlighted (list[tuple[int, int]], optional): Positions to be highlighted. Defaults to None.
        """
        for row in range(dimensions[0]):
            for col in range(dimensions[1]):
                position = (row, col)
                tile = board.get_tile(position)
                colour = self.get_tile_color(tile)
                if colour and (not highlighted or position not in highlighted):
                    self.color_cell(position, colour)

    def annotate_buildings(self, board: Board, dimensions: tuple[int, int]) -> None:
        """
        Annotates the buildings on the board with their current health values.

        Args:
            board (Board): The current game board.
            dimensions (tuple[int, int]): The dimensions of the board.
        """
        for row in range(dimensions[0]):
            for col in range(dimensions[1]):
                position = (row, col)
                tile = board.get_tile(position)
                if isinstance(tile, Building) and not tile.is_destroyed():
                    self.annotate_position(position, str(tile), font=ENTITY_FONT)

    def annotate_entities(self, entities: list[Entity]) -> None:
        """
        Annotates the positions of entities on the board with their display symbols.

        Args:
            entities (list[Entity]): A list of all entities on the board.
        """
        for entity in entities:
            position = entity.get_position()
            display = self._get_display_symbol(entity)
            self.annotate_position(position, display, font=ENTITY_FONT)

    def get_tile_color(self, tile: Tile) -> str:
        """
        Determines the color of a given tile based on its type.

        Args:
            tile (Tile): The tile whose color needs to be determined.

        Returns:
            str: The color associated with the tile type.
        """
        if isinstance(tile, Ground):
            return GROUND_COLOR
        elif isinstance(tile, Mountain):
            return MOUNTAIN_COLOR
        elif isinstance(tile, Building):
            return DESTROYED_COLOR if str(tile) == '0' else BUILDING_COLOR
        return None

    def _get_display_symbol(self, entity: Entity) -> str:
        """
        Get the display symbol for the given entity.
        
        Args:
            entity (Entity): The entity whose display text needs to be determined.

        Returns:
            str: The display text associated with the entity type.
        """
        if isinstance(entity, TankMech):
            return TANK_DISPLAY
        elif isinstance(entity, HealMech):
            return HEAL_DISPLAY
        elif isinstance(entity, Scorpion):
            return SCORPION_DISPLAY
        elif isinstance(entity, Firefly):
            return FIREFLY_DISPLAY

    def bind_click_callback(self, 
                            click_callback: Callable[[tuple[int, int]],None]) -> None:
        """
        Binds the <Button-1> and <Button-2> events on itself to a function that calls the provided
        click handler at the correct position.

        Note: We bind both <Button-1> and <Button-2> to account for differences between Windows
        and Mac operating systems.

        Note: Handling callbacks is an advanced task. These callbacks will be created within the
        controller, as this is the only place where you have access to the required modeling
        information. Integrate GameGrid into the game before attempting this method.

        Args:
            click_callback (Callable[[tuple[int, int]], None]): The callback function to be executed
                when a click event occurs. It takes a tuple of integers representing the (row, column)
                position of the click.
        """
        click_event = lambda event: click_callback(self.pixel_to_cell(event.x, event.y))
        self.bind("<Button-1>", click_event)
        self.bind("<Button-2>", click_event)

class SideBar(AbstractGrid):
    """
    SideBar inherits from AbstractGrid provided in a2 support.py. SideBar is a view component
    that displays properties of each entity. Entities appear in descending priority order, with the highest
    priority entity appearing at the top of the sidebar, and the lowest priority entity appearing at the
    bottom of the sidebar. A Sidebar object is a grid with 4 columns. The top row displays the text
    "Unit" in the first column, "Coord" in the second column, "Hp" in the third column, and "Dmg"
    in the fourth column. The SideBar maintains a constant height, but the number of rows will vary
    depending on the number of entities remaining in the game. Rows should expand out to fill available
    space. You do not need to handle visual artifacts caused by too many rows being present. An
    example of a completed SideBar is presented in Figure 5.
    """
    def __init__(self, master: tk.Widget,dimensions: tuple[int, int], size: tuple[int, int]) -> None:
        """
        Instantiates a SideBar with the specified dimensions and size.

        Args:
            master (tk.Widget): The parent widget.
            dimensions (tuple[int, int]): The dimensions of the sidebar grid.
            size (tuple[int, int]): The size of the sidebar in pixels.

        Returns:
            None
        """
        super().__init__(master, dimensions,size)

    def display(self, entities: list[Entity]) -> None:
        """
        Clears the sidebar, then redraws the header followed by the relevant properties of the given
        entities on the SideBar instance itself.

        Args:
            entities (list[Entity]): A list of entities to be displayed on the sidebar.

        Returns:
            None
        """
        self.clear()  # Clear the sidebar

        self._dimensions = (len(entities) + 1,4)

        for col, heading in enumerate(SIDEBAR_HEADINGS):
            self.annotate_position((0, col), heading, font=SIDEBAR_FONT)

        # Display entities
        for row, entity in enumerate(entities, start=1):
            # Get entity properties
            symbol = self._get_display_symbol(entity)
            position = entity.get_position()
            health = entity.get_health()
            damage = entity.get_strength()

            # Annotate entity properties in the sidebar
            self.annotate_position((row, 0), symbol, font=ENTITY_FONT)
            self.annotate_position((row, 1), f"{position}", font=SIDEBAR_FONT)
            self.annotate_position((row, 2), str(health), font=SIDEBAR_FONT)
            self.annotate_position((row, 3), str(damage), font=SIDEBAR_FONT)

    def _get_display_symbol(self, entity: Entity) -> str:
        """
        Get the display symbol for the given entity.

        Args:
            entity (Entity): The entity for which to determine the display symbol.

        Returns:
            str: The display symbol corresponding to the entity.
        """
        if isinstance(entity, TankMech):
            return TANK_DISPLAY
        elif isinstance(entity, HealMech):
            return HEAL_DISPLAY
        elif isinstance(entity, Scorpion):
            return SCORPION_DISPLAY
        elif isinstance(entity, Firefly):
            return FIREFLY_DISPLAY

class ControlBar(tk.Frame):
    """
    ControlBar inherits from tk.Frame. ControlBar is a view component that contains three buttons
    that allow the user to perform administration actions. In order from left to right, the ControlBar
    contains a save, load, and end turn button.
    """
    def __init__(self, master: tk.Widget, 
                 save_callback: Optional[Callable[[], None]] = None, 
                 load_callback: Optional[Callable[[], None]] = None, 
                 turn_callback: Optional[Callable[[], None]] = None, 
                 **kwargs) -> None:
        """
        Instantiates a ControlBar as a special kind of frame with the desired button layout.

        Args:
            master (tk.Widget): The parent widget.
            save_callback (Optional[Callable[[], None]]): The callback function for the save button.
            load_callback (Optional[Callable[[], None]]): The callback function for the load button.
            turn_callback (Optional[Callable[[], None]]): The callback function for the end turn button.
            **kwargs: Additional keyword arguments to pass to the tk.Frame constructor.

        Returns:
            None
        """
        super().__init__(master, **kwargs)
        
        # Create save button
        save_button = tk.Button(self, text=SAVE_TEXT, command=save_callback)

        # Create load button
        load_button = tk.Button(self, text=LOAD_TEXT, command=load_callback)

        # Create end turn button
        turn_button = tk.Button(self, text=TURN_TEXT, command=turn_callback)

        load_button.pack(expand=tk.TRUE, side=tk.LEFT)
        save_button.pack(expand=tk.TRUE, side=tk.LEFT)
        turn_button.pack(expand=tk.TRUE, side=tk.LEFT)

class BreachView():
    """
    The BreachView class provides a wrapper around the smaller GUI components, providing a single view interface for the controller.
    """
    def __init__(self,
                 root: tk.Tk,
                 board_dims: tuple[int, int],
                 save_callback: Optional[Callable[[], None]] = None,
                 load_callback: Optional[Callable[[], None]] = None,
                 turn_callback: Optional[Callable[[], None]] = None) -> None:
        """
        Instantiates the view. Sets title of the given root window, and instantiates all child components.
        The buttons on the instantiated ControlBar receive the given callbacks as their respective commands.

        Args:
            root (tk.Tk): The root window.
            board_dims (tuple[int, int]): The dimensions of the game board.
            save_callback (Optional[Callable[[], None]]): Callback function for saving the game.
            load_callback (Optional[Callable[[], None]]): Callback function for loading a saved game.
            turn_callback (Optional[Callable[[], None]]): Callback function for ending the current turn.

        Returns:
            None
        """
        self.root = root
        
        root.title(BANNER_TEXT)

        # Create and pack the banner
        self.banner = tk.Label(root, text=BANNER_TEXT, font=BANNER_FONT)
        self.banner.pack(side=tk.TOP, fill=tk.X)

        # Create a container frame for the GameGrid and Sidebar
        self.container = tk.Frame(root)
        self.container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create and pack the GameGrid
        self.game_grid = GameGrid(self.container,board_dims,(GRID_SIZE,GRID_SIZE))

        # Create and pack the SideBar
        self.sidebar = SideBar(self.container,board_dims,(SIDEBAR_WIDTH,GRID_SIZE))

        # Create and pack the ControlBar
        self.control_bar = ControlBar(root, save_callback, load_callback, turn_callback)

        self.game_grid.pack(side=tk.LEFT, expand=tk.TRUE)
        self.sidebar.pack(side=tk.LEFT, expand=tk.TRUE)
        self.control_bar.pack(expand=True,fill=tk.BOTH)

    def bind_click_callback(self, click_callback: Callable[[tuple[int, int]], None]) -> None:
        """
        Binds a click event handler to the instantiated GameGrid based on click_callback.

        Args:
            click_callback (Callable[[tuple[int, int]], None]): The callback function for handling click events.

        Returns:
            None
        """
        self.game_grid.bind_click_callback(click_callback)

    def redraw(self, board: Board, entities: list[Entity], 
               highlighted: list[tuple[int, int]] = None, movement: bool = False) -> None:
        """
        Redraws the instantiated GameGrid and SideBar based on the given board, list of entities, and tile highlight information.

        Args:
            board (Board): The game board.
            entities (list[Entity]): The list of entities.
            highlighted (list[tuple[int, int]], optional): List of positions to highlight on the grid.
            movement (bool, optional): Whether entities are currently in movement state.

        Returns:
            None
        """
        self.game_grid.redraw(board, entities, highlighted, movement)
        self.sidebar.display(entities)

class IntoTheBreach:
    """
    IntoTheBreach is the controller class for the overall game. It's responsible for creating and maintaining instances of the model and view classes,
    event handling, and facilitating communication between the model and view classes.
    """
    def __init__(self, root: tk.Tk, game_file: str) -> None:
        """
        Instantiates the controller. Creates instances of BreachModel and BreachView, and redraws the display to show the initial game state.
        IO errors when loading a board from the game file are not handled during this function.

        Args:
            root (tk.Tk): The root window.
            game_file (str): The path to the game file.

        Returns:
            None
        """
        self._root = root
        self.focussed_entity = None
        self._game_file = game_file
        self.load_model(game_file)
        self._view = BreachView(self._root, self._model.get_board().get_dimensions(),self.save_game,self.load_game,self.end_turn)
        self._view.bind_click_callback(self.handle_click)
        self.redraw()


    def redraw(self) -> None:
        """
        Redraws the view based on the state of the model and the current focussed entity.

        Returns:
            None
        """
        self._view.redraw(self._model.get_board(), self._model.get_entities())

    def set_focussed_entity(self, entity: Optional[Entity]) -> None:
        """
        Sets the given entity to be the one on which to base highlighting. Or clears the focussed entity if None is given.

        Args:
            entity (Optional[Entity]): The entity to set as the focussed entity.

        Returns:
            None
        """
        if entity:
            self.focussed_entity = entity
        else:
            self.focussed_entity = None

    def make_move(self, position: tuple[int, int]) -> None:
        """
        Attempts to move the focussed entity to the given position, and then clears the focussed entity.
        Note that you have implemented a method in BreachModel that enforces the validity of a move according to the game rules already.

        Args:
            position (tuple[int, int]): The position to move the focussed entity to.

        Returns:
            None
        """
        if self.focussed_entity:
            self._model.attempt_move(self.focussed_entity, position)\

    def load_model(self, file_path: str) -> None:
        """
        Replaces the current game state with a new state based on the provided file.

        Args:
            file_path (str): The path to the file containing the game state.

        Returns:
            None
        """
        try:
            with open(file_path, 'r') as file:
                content = file.read().strip()

                board_data, entity_data = content.split('\n\n')

                board = [list(line) for line in board_data.split('\n')]

                entities = []
                for line in entity_data.split('\n'):
                    entity_type, x, y, health, speed, strength = line.split(',')
                    position = (int(x),int(y))
                    health = int(health)
                    speed = int(speed)
                    strength = int(strength)
                    if entity_type == TANK_SYMBOL:
                        entities.append(TankMech(position, health, speed, strength))
                    elif entity_type == HEAL_SYMBOL:
                        entities.append(HealMech(position, health, speed, strength))
                    elif entity_type == SCORPION_SYMBOL:
                        entities.append(Scorpion(position, health, speed, strength))
                    elif entity_type == FIREFLY_SYMBOL:
                        entities.append(Firefly(position, health, speed, strength))

            # Update model with loaded game state
            self._model = BreachModel(Board(board), entities)
            
        except IOError as e:
            # Display error message box
            messagebox.showerror(IO_ERROR_TITLE, IO_ERROR_MESSAGE + e)

    def save_game(self) -> None:
        """
        Saves the current game state to a file.

        Returns:
            None
        """
        if self._model.ready_to_save():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                try:
                    with open(file_path, 'w') as file:
                        file.write(str(self._model._board))
                        file.write('\n\n')
                        for entity in self._model.get_entities():
                            file.writelines(str(entity) + "\n")
                except Exception as e:
                    messagebox.showerror(INVALID_SAVE_TITLE, f"An error occurred while saving the file: {e}")
        else:
            messagebox.showerror(INVALID_SAVE_TITLE, INVALID_SAVE_MESSAGE)

    def load_game(self) -> None:
        """
        Loads a new game state from a file.

        Returns:
            None
        """
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.load_model(file_path)
            self._game_file = file_path
            self.redraw()

    def end_turn(self) -> None:
        """
        Executes the attack phase, enemy movement phase, and termination checking according to game rules.

        Returns:
            None
        """
        self._model.end_turn()
        self.redraw()
        if self._model.has_won():
            if messagebox.askokcancel("You Win!", "You Win! " + PLAY_AGAIN_TEXT):
                self.load_model(self._game_file)
                self.redraw()

            else:
                self._root.destroy()
        if self._model.has_lost():
            if messagebox.askokcancel("You Lost!", "You Lost! " + PLAY_AGAIN_TEXT):
                self.load_model(self._game_file)
                self.redraw()

            else:
                self._root.destroy()

    def handle_click(self, position: tuple[int, int]) -> None:
        """
        Handle click events on the game grid.
        """
        selected_entity = self._model.entity_positions().get(position)

        if self.focussed_entity:
        # Already selected an entity
            if isinstance(selected_entity, Mech) and selected_entity != self.focussed_entity:
                self._view.redraw(self._model.get_board(), self._model.get_entities(), self._model.get_valid_movement_positions(selected_entity), True)
            elif isinstance(selected_entity, Enemy) and selected_entity != self.focussed_entity:
                self._view.redraw(self._model.get_board(), self._model.get_entities(), selected_entity.get_targets())
            elif isinstance(self.focussed_entity, Mech) and self.focussed_entity.is_active():
                # Attempt move if the Mech is active
                self.make_move(position)
                self.redraw()
            else:
                self.redraw()

            self.set_focussed_entity(selected_entity)
        else:
            # Set focussed entity and show movement range
            self.set_focussed_entity(selected_entity)
            if isinstance(self.focussed_entity, Entity):
                self.show_movement_range()

    def show_movement_range(self) -> None:
        """Show movement range of the focussed entity."""
        if isinstance(self.focussed_entity, Mech):
            if self.focussed_entity.is_active():
                self._view.redraw(self._model.get_board(), self._model.get_entities(), self._model.get_valid_movement_positions(self.focussed_entity), True)
            else:
                self._view.redraw(self._model.get_board(), self._model.get_entities(), self.focussed_entity.get_targets())
        else:
            self._view.redraw(self._model.get_board(), self._model.get_entities(), self.focussed_entity.get_targets())
                
def play_game(root: tk.Tk, file_path: str):
    """
    Constructs the controller instance and starts the event loop.
    """
    IntoTheBreach(root, file_path)
    root.mainloop()

def main() -> None:
    """The main function"""
    root = tk.Tk()
    play_game(root, "levels/level1.txt")
    pass

if __name__ == "__main__":
    main()