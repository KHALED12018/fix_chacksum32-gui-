import binascii
import tkinter as tk
from tkinter import filedialog

TABLE = [0] * 256
INIT_VAL = 0xFFFFFFFF
XOR_OUT = 0xFFFFFFFF
POLY = 0x04C11DB7

def calculate_checksum(filename):
    # Open the binary file in read mode
    with open(filename, 'rb') as f:
        data = f.read()
        
    # Initialize the checksum to the INIT_VAL
    checksum = INIT_VAL
    
    # Calculate the checksum for the file
    for byte in data:
        index = (checksum ^ byte) & 0xff
        checksum = (checksum >> 8) ^ TABLE[index]
    
    return checksum

def browse_file():
    # Open a file dialog to choose a binary file
    filename = filedialog.askopenfilename()
    
    if filename:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)

def install_checksum():
    # Get the filename from the entry
    filename = file_entry.get()
    
    # Calculate the new checksum
    new_checksum = calculate_checksum(filename)
    
    # Convert the user-provided checksum to an integer
    user_checksum = int(checksum_entry.get(), 16)
    
    # Calculate the new checksum value including the user-provided checksum
    full_checksum = (new_checksum + user_checksum) & 0xFFFFFFFF
    
    # Convert the checksum to a byte string and reverse the order of the bytes
    checksum_bytes = binascii.unhexlify('{:08x}'.format(full_checksum))
    checksum_bytes = checksum_bytes[::-1]
    
    # Install the new checksum on the original file
    with open(filename, 'r+b') as f:
        f.seek(-4, 2)
        f.write(checksum_bytes)
    
    # Save the protected file with the original filename
    with open(filename, 'rb') as f:
        data = f.read()
    with open(filename, 'wb') as f:
        f.write(data)
    
    # Print the new checksum in the result entry
    result_entry.delete(0, tk.END)
    result_entry.insert(0, checksum_bytes.hex())

# Create the GUI
root = tk.Tk()
root.title('Cksum32_gui by Dragon-Noir2023 ')
root.geometry('400x200')

# Create the file selection section
file_label = tk.Label(root, text='Binary File :')
file_label.grid(row=0, column=0, padx=5, pady=5)
file_entry = tk.Entry(root)
file_entry.grid(row=0, column=1, padx=5, pady=5)
browse_button = tk.Button(root, text='Browse', command=browse_file)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# Create the checksum entry section
checksum_label = tk.Label(root, text='Checksum32 :')
checksum_label.grid(row=1, column=0, padx=5, pady=5)
checksum_entry = tk.Entry(root)
checksum_entry.grid(row=1, column=1, padx=5, pady=5)

# Create the result section
result_label = tk.Label(root, text='Result :')
result_label.grid(row=3, column=0, padx=5, pady=5)
result_entry = tk.Entry(root)
result_entry.grid(row=3, column=1, padx=5, pady=5)

# Create the install button
install_button = tk.Button(root, text='Fix Checksum', command=install_checksum)
install_button.grid(row=2, column=1, padx=5, pady=5)

root.mainloop()