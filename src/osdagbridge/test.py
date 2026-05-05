from osdag_core.design_type.tension_member.tension_bolted import Tension_bolted
from osdag_core.cli import (
    _get_design_dictionary,
    _get_output_dictionary
)

osi_path = r"C:\Users\1hasa\Documents\tension.osi"
design_dict = _get_design_dictionary(osi_path)
tension =  Tension_bolted()
tension.set_osdaglogger(None, None)
val_errors = tension.func_for_validation(design_dict)
if val_errors:
    print("Validation Errors:")

out_dict = _get_output_dictionary(tension)
print(out_dict)