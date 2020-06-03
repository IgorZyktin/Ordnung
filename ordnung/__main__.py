# -*- coding: utf-8 -*-

"""Server starter.
"""
import uvicorn

from ordnung import settings


def main():
    """Main flow.
    """
    uvicorn.run(
        "ordnung.presentation.app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        root_path='http://84.201.137.8'
    )


if __name__ == '__main__':
    main()
