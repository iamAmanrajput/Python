def serve_chai(flavor):
    try:
        print(f"Preparing {flavor} chai...")
        if flavor == "unknown":
            raise ValueError("We don't know that flavor")
    except ValueError as e:
        print("Error: ", e)
    else:
        print(f"{flavor} chai is served")
    finally:
        print("Next customer please")

serve_chai("masala")
serve_chai("unknown")

# output

# Preparing masala chai...
# masala chai is served
# Next customer please

# Preparing unknown chai...
# Error:  We don't know that flavor
# Next customer please
