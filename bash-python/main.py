import argparse

def main(args):
  args
  

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-mode", help="mode flag[description]")
  args = parser.parse_args()
  print(f"args: {args}")
  main(args)