import argparse
import os
import server.FileService as FileService

def main():

    parser = argparse.ArgumentParser(description="FileService")
    parser.add_argument('-d', '--dir', default=os.path.join(os.getcwd(), 'data'), type=str,
                        help="working directory (default: 'data')")

    params = parser.parse_args()

    work_dir = params.dir if os.path.isabs(params.dir) else os.path.join(os.getcwd(), params.dir)
    FileService.change_dir(work_dir)

if __name__ == '__main__':
    main()
