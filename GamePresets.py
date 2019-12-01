class GamePresets:

    def __init__(self):
        preset0 = [8,
                   [
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]
                    ]
                   ]

        self.presets = []
        self.presets.append(preset0)


def main():
    preset = GamePresets()
    print(preset.presets[0])
    print(preset.presets[0][0])

    for x in preset.presets[0][1]:
        for y in x:
            print(y)

if __name__ == '__main__':
    main()
