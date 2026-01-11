import asyncio

async def brew_chai():
    print("Boiling water...")
    await asyncio.sleep(2)  # Simulate time taken to boil water
    print("Steeping the tea...")
    await asyncio.sleep(3)  # Simulate time taken to steep tea
    print("Adding milk and sugar...")
    await asyncio.sleep(1)  # Simulate time taken to add milk and sugar
    print("Chai is ready!")

asyncio.run(brew_chai())

#output
# Boiling water...
# Steeping the tea...
# Adding milk and sugar...
# Chai is ready!