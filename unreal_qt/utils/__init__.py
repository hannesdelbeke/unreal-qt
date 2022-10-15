def install_to_menu():
    import unreal_menu
    data = {
        "parent_menu": "LevelEditor.MainMenu.Tools",
        "items": [
            {
                "name": "Qt Utils",
                "items": [
                    {
                        "name": "Icon Browser",
                        "items": [
                            {
                                "name": "Open Icon Browser",
                                "command": "import unreal_qt.utils.icons;"
                                           "unreal_qt.utils.icons.show()"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    unreal_menu.setup_menu(data)