from simplexss.utils.di import (
    containers,
    dependencies
)


class GUIContainer(containers.Container):
    main_page = dependencies.Dependency()
