import plural

nouns = [
    "apple", "balloon", "river", "mountain", "chair", "table", "computer", "phone",
    "book", "pen", "pencil", "notebook", "lamp", "bottle", "cup", "window", "door",
    "car", "bicycle", "train", "airplane", "cloud", "rain", "snow", "sun", "moon",
    "star", "planet", "galaxy", "ocean", "lake", "beach", "forest", "tree", "flower",
    "grass", "leaf", "root", "soil", "rock", "sand", "animal", "dog", "cat", "bird",
    "fish", "horse", "lion", "tiger", "elephant", "bear", "fox", "rabbit", "frog",
    "insect", "spider", "bee", "ant", "butterfly", "mushroom", "food", "bread", "cheese",
    "meat", "fruit", "vegetable", "rice", "pasta", "soup", "salad", "drink", "water",
    "juice", "coffee", "tea", "chocolate", "dessert", "cake", "cookie", "ice cream",
    "school", "teacher", "student", "classroom", "desk", "library", "playground",
    "hospital", "doctor", "nurse", "medicine", "vehicle", "engine", "wheel", "road",
    "bridge", "city", "country", "village", "park"
]


for noun in nouns:
    print(    plural.PluralEngine.pluralize(noun))