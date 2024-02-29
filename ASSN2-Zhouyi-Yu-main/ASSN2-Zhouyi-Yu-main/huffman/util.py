import bitio
import huffman
import pickle


def read_tree(tree_stream):
    # '''Read a description of a Huffman tree from the given compressed
    # tree stream, and use the pickle module to construct the tree object.
    # Then, return the root node of the tree itself.

    # Args:
    #   tree_stream: The compressed stream to read the tree from.

    # Returns:
    #   A Huffman tree root constructed according to the given description.
    # '''
    readObj = pickle.load(tree_stream)
    return readObj


def decode_byte(tree, bitreader):
    # """
    # Reads bits from the bit reader and traverses the tree from
    # the root to a leaf. Once a leaf is reached, bits are no longer read
    # and the value of that leaf is returned.

    # Args:
    #   bitreader: An instance of bitio.BitReader to read the tree from. - the compressed data
    #   tree: A Huffman tree. - the tree to decode bitreader

    # Returns:
    #   Next byte of the compressed bit stream.

    if isinstance(tree, huffman.TreeLeaf):
      return tree.getValue()
    node = tree
    while True:
      if isinstance(node, huffman.TreeLeaf): 
          return node.getValue()
      bit = bitreader.readbit()
      if bit == 1:
          node = node.getRight()
      elif bit == 0:
          node = node.getLeft()
    


def decompress(compressed, uncompressed):
    # '''First, read a Huffman tree from the 'compressed' stream using your
    # read_tree function. Then use that tree to decode the rest of the
    # stream and write the resulting symbols to the 'uncompressed'
    # stream.
    
    # Args:
    #   compressed: A file stream from which compressed input is read.
    #   uncompressed: A writable file stream to which the uncompressed
    #       output is written.
    # '''

    bitreader = bitio.BitReader(compressed)
    tree = read_tree(compressed)
    bitwriter = bitio.BitWriter(uncompressed)
  
    endOfDecode = False
    byte = decode_byte(tree, bitreader)
    
    while byte != None:
      bitwriter.writebits(byte, 8)
      byte = decode_byte(tree, bitreader)



def write_tree(tree, tree_stream):
    # '''Write the specified Huffman tree to the given tree_stream
    # using pickle.

    # Hint:  Use pickle.dump()
    # **Requirement:**  pickle.dump(..., protocol=4)

    # Args:
    #   tree: A Huffman tree.
    #   tree_stream: The binary file to write the tree to.
    # '''
    pickle.dump(tree, tree_stream, protocol=4)


def compress(tree, uncompressed, compressed):
#     '''First write the given tree to the stream 'compressed' using the
#     write_tree function. Then use the same tree to encode the data
#     from the input stream 'uncompressed' and write it to 'compressed'.
#     If there are any partially-written bytes remaining at the end,
#     write 0 bits to form a complete byte.

#     Flush the bitwriter after writing the entire compressed file.

#     Args:
#       tree: A Huffman tree.
#       uncompressed: A file stream from which you can read the input.
#       compressed: A file stream that will receive the tree description
#           and the coded input data.

#     '''

    write_tree(tree, compressed)
    table = huffman.make_encoding_table(tree)
    bitwriter = bitio.BitWriter(compressed)
    bitreader = bitio.BitReader(uncompressed)
    EOF = False
    while not EOF:
      try:
        byte = bitreader.readbits(8)
        encoded = table[byte]
        for bit in encoded:
          bitwriter.writebit(bit)
      except EOFError:
        EOF = True
        encoded = table[None]
        for bit in encoded:
           bitwriter.writebit(bit)
    bitwriter.flush()
