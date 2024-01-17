# DINRailHubTestFirmware
USB boot tool run NXP uuu tool to program the firmware, and boot M7 core from eMMC(emmc_burn_indus_fw.lst), ram(ram_burn_indus_fw.lst) or ddr(ddr_burn_indus_fw.lst).

Run ram_run.bat to program and run M7 firmware from ram:
1. Copy the target firmware file to the folder /usb_boot_tool.
2. Open ram_run.bat and modify the target firmware file name that will be programmed to board, e.g. hal_eth_test_app.bin:
   .\uuu.exe -b ram_burn_indus_fw.lst imx-boot hal_eth_test_app.bin

3. Switch the boot mode to USB serial download.
  1 - ON
  2 - ON
  3 - OFF
  4 - OFF
4. Reset the board.
5. Double click ram_run.bat to start the programming
6. The programming result will show as below:

   uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.5.21-0-g1f42172
   
   Success 1    Failure 0
   
   2:18     5/ 5 [Done                                  ] FB: done
   2:7      1/ 1 [=================100%=================] SDPS: boot -scanterm -f imx-boot -scanlimited 0x800000

Run ddr_run.bat to program and run M7 firmware from ddr:
1. Copy the target firmware file to the folder /usb_boot_tool.
2. Open ddr_run.bat and modify the target firmware file name that will be programmed to board, e.g. hal_eth_test_app.bin:
  
   .\uuu.exe -b ddr_burn_indus_fw.lst imx-boot hal_eth_test_app.bin

3. Switch the boot mode to USB serial download.
  1 - ON
  2 - ON
  3 - OFF
  4 - OFF
4. Reset the board.
5. Double click ddr_run.bat to start the programming
6. The programming result will show as below:

   uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.5.21-0-g1f42172
   
   Success 1    Failure 0
   
   2:18     5/ 5 [Done                                  ] FB: done
   2:7      1/ 1 [=================100%=================] SDPS: boot -scanterm -f imx-boot -scanlimited 0x800000
