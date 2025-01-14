# Author: Brother Keers

def main():
  # Open the file in read mode.
  with open('sentence.txt', 'r') as f:
    # Read the content of the file.
    content = f.read()

  # Print the content of the file to the terminal.
  print(content)

# Run this script if it was called directly and not imported by another script.
if __name__ == "__main__":
  main()