Add physical disk

To assign ownership of a replacement disk: 
Login to the netapp controller that needs to own the disk 
Run 'disk show -n' to get a list of unowned disks and the ID 
Run 'disk assign #x.## -o netapp#' to assign the disk 
Run 'disk show -n' again to verify there are no unowned disks 
disk show -a will show all disks 
