from multiprocessing import Process, Queue

def prepare_chai(queue):
    """
    This function runs in a separate process.
    It prepares chai and sends the result back
    to the main process using a Queue.
    """
    queue.put("Masala chai is ready")  # Send data to parent process




if __name__ == "__main__":
    # Queue is used for inter-process communication (IPC)
    # Processes cannot share memory directly like threads
    queue = Queue()

    # Create a separate process
    p = Process(target=prepare_chai, args=(queue,))

    # Start the process
    p.start()

    # Wait for the process to finish
    p.join()

    # Receive data sent from the child process
    print(queue.get())

# Masala chai is ready

