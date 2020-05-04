# -*- coding: utf-8 -*-

"""Server starter.
"""
import uvicorn

from ordnung.presentation import presentation_settings


def main():
    """Main flow.
    """
    uvicorn.run(
        "ordnung.presentation.app:app",
        host=presentation_settings.HOST,
        port=presentation_settings.PORT,
        reload=presentation_settings.RELOAD
    )


if __name__ == '__main__':
    main()
