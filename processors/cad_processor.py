import ezdxf
from ezdxf import recover

def process_dxf(file_path):
    """
    Process a DXF file to extract basic information.
    Attempts standard reading first; if that fails, uses recovery mode.
    Returns a dictionary with metadata such as the number of entities and extents,
    or an error message if processing fails.
    """
    try:
        # Try reading the file normally
        doc = ezdxf.readfile(file_path)
    except ezdxf.DXFStructureError as e:
        # If there's a structure error, try to recover the file
        try:
            doc, auditor = recover.readfile(file_path)
            # auditor can be used to check for errors if needed
        except Exception as rec_e:
            return {"error": f"Recovery failed: {rec_e}"}
    except Exception as e:
        return {"error": str(e)}
    
    msp = doc.modelspace()
    num_entities = len(msp)
    extents = (doc.header.get("$EXTMIN"), doc.header.get("$EXTMAX"))
    
    return {"number_of_entities": num_entities, "extents": extents}
