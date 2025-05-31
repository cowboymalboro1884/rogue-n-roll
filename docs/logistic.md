# Логическая структура

```mermaid
classDiagram
    class GameObject {
        +x : int
        +y : int
        +char : char
        +color : Color
        +name : string
        +isBlocking : bool
        +isWalkable : bool
        +draw(renderer)
    }

    class Entity {
        <<Abstract>>
        +stats : Stats
        +inventory : Inventory
        +aiComponent : AIComponent
        +combatComponent : CombatComponent
        +pickup(item)
        +attack(target)
        +move(dx, dy)
        +isAlive() bool
    }
    GameObject <|-- Entity

    class Player {
        +activeQuests : List~Quest~
    }
    Entity <|-- Player

    class Monster {
        +monsterType : MonsterType
    }
    Entity <|-- Monster

    class Item {
        +onUse(user: Entity)
        +onEquip(user: Entity)
        +onUnequip(user: Entity)
    }
    GameObject <|-- Item

    class Equipment {
        +slot : EquipmentSlot
        +statModifiers : Map~Stat, int~
    }
    Item <|-- Equipment


    class Stats {
        +maxHp : int
        +currentHp : int
        +attackPower : int
        +defense : int
        +getEffectiveStat(stat: Stat) : int
    }

    class Inventory {
        +items : List~Item~
        +equippedItems : Map~EquipmentSlot, Equipment~
        +addItem(item)
        +removeItem(item)
        +equipItem(item)
        +unequipItem(slot)
    }

    class Tile {
        +type : TileType (WALL, FLOOR, DOOR)
        +isExplored : bool
    }
    GameObject <|-- Tile

    class GameMap {
        +width : int
        +height : int
        +tiles : Tile[][]
        +entitiesOnMap : List~Entity~
        +itemsOnMap : Map~Point, List~Item~ ~
        +getTile(x, y)
        +isBlocked(x, y)
    }

    class GameManager {
        +player : Player
        +currentMap : GameMap
        +gameState : GameState
        +gameLoop()
        +processInput(key)
        +updateAI()
    }

    class MapGenerator {
        +generateMap(width, height, params) : GameMap
        +loadMapFromFile(filePath) : GameMap
    }

    class ConsoleRenderer {
        +renderMap(map: GameMap)
        +renderEntities(entities: List~Entity~)
        +renderUI(player: Player)
        +displayMessage(message: string)
    }

    class Quest {
        +title : string
        +description : string
        +objectives : List~Objective~
        +rewards : List~Reward~
        +isCompleted : bool
        +updateProgress(event)
    }

    class QuestManager {
        +activeQuests : List~Quest~
        +availableQuests : List~QuestTemplate~
        +generateSideQuest() : Quest
        +addQuest(quest)
        +updateQuests(event)
    }

    Entity "1" -- "1" Stats
    Entity "1" -- "1" Inventory
    Player "1" -- "*" Quest : знает о
    GameManager "1" -- "1" Player
    GameManager "1" -- "1" GameMap
    GameManager "1" -- "1" ConsoleRenderer
    GameManager "1" -- "1" QuestManager
    GameMap "1" -- "*" Tile : состоит из
    GameMap "1" -- "*" Entity : содержит
    GameMap "1" -- "*" Item : содержит
    MapGenerator ..> GameMap : создает

    Item "*" -- "1" Entity : может быть использован
    Equipment "*" -- "1" Entity : может быть экипирован
```

# Описание

Описание классов:

- **GameObject**: Базовый класс для всех объектов, имеющих представление на карте (координаты, символ, цвет).
- **Entity**: Абстрактный класс для всех "живых" существ (игрок, монстры). Содержит характеристики (Stats), инвентарь (Inventory), компоненты поведения (AI, бой).
- **Player**: Представляет персонажа игрока. Наследуется от Entity, добавляет специфичные для игрока данные (например, активные квесты).
- **Monster**: Представляет монстра. Наследуется от Entity, может иметь тип, специфичное поведение.
- **Item**: Базовый класс для всех предметов. Может быть использован, подобран.
- **Equipment**: Подкласс Item, представляющий экипируемые предметы (оружие, броня). Имеет слот экипировки и модификаторы характеристик.
- **Stats**: Хранит и управляет характеристиками сущности (здоровье, сила и т.д.). Может учитывать эффекты от экипировки/баффов.
- **Inventory**: Управляет предметами, которые несет сущность, и теми, что надеты.
- **Tile**: Представляет одну клетку карты (стена, пол, дверь и т.д.).
- **GameMap**: Хранит двумерный массив тайлов, а также списки сущностей и предметов, находящихся на карте.
- **GameManager**: Оркестрирует основной игровой процесс, управляет состоянием игры.
- **MapGenerator**: Отвечает за создание и загрузку объектов GameMap.
- **ConsoleRenderer**: Отвечает за отображение игрового мира и интерфейса в консоли.
- **Quest**: Представляет задание с целями, описанием и наградами.
- **QuestManager**: Управляет жизненным циклом квестов, включая их генерацию.
