
for kit in .kits:

    kit_name = "%s_%s%s_%s" % (kit.vendor, kit.kit, kit.subkit, kit.version)
    
    for adapter in kit:
        print(">%s-%s\n%s\n" % (kit_name, adapter.barcode, adapter.full_sequence)


