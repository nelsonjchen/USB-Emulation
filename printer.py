import datetime
from hexdump import hexdump
from USBIP import BaseStucture, USBDevice, InterfaceDescriptor, DeviceConfigurations, EndPoint, USBContainer

# Emulating USB Thermal Printer

# Configuration Descriptor
configuration = DeviceConfigurations(
    bLength=0x09,
    bDescriptorType=0x02,
    wTotalLength=0x0020,
    bNumInterfaces=0x01,
    bConfigurationValue=0x01,
    iConfiguration=0x00,
    bmAttributes=0xC0,  # -> Self Powered
    bMaxPower=0x01  # 2 mA
)

interface_d = InterfaceDescriptor(
    bLength=0x09,
    bDescriptorType=0x04,
    bInterfaceNumber=0x00,
    bAlternateSetting=0x00,
    bNumEndpoints=0x02,
    bInterfaceClass=0x07,  # -> This is a Printer USB Device Interface Class
    bInterfaceSubClass=0x01,
    bInterfaceProtocol=0x02,
    iInterface=0x00
)

# Endpoint Descriptor
end_point_out = EndPoint(
    bLength=0x07,
    bDescriptorType=0x05,
    bEndpointAddress=0x01,  # -> Direction: IN - EndpointID: 2
    bmAttributes=0x02,  # -> Bulk transfer Type
    wMaxPacketSize=0x0040,
    bInterval=0x00
)

# Endpoint Descriptor
end_point_in = EndPoint(
    bLength=0x07,
    bDescriptorType=0x05,
    bEndpointAddress=0x82,  # -> Direction: IN - EndpointID: 2
    bmAttributes=0x02,  # -> Bulk transfer Type
    wMaxPacketSize=0x0040,
    bInterval=0x00
)

interface_d.endpoints = [end_point_out, end_point_in]
interface_d.descriptions = []
configuration.interfaces = [interface_d]


class USBPrinter(USBDevice):
    bLength=0x12
    bNumInterfaces = 0x1
    bConfigurationValue = 0x1
    bcdUSB = 0x0200
    bDeviceClass = 0x0  # -> This is an Interface Class Defined Device
    bDeviceSubClass = 0x0
    bDeviceProtocol = 0x0
    bMaxPacketSize0 = 0x40,
    # idVendor = Seiko Epson Corp.
    vendorID = 0x04B8
    # idProduct
    productID = 0x0E02
    bcdDevice = 0x0100
    # iManufacturer .. not sure
    # iProduct .. not sure
    # iSerialNumber .. not sure
    bNumConfigurations = 0x1
    configurations = [configuration]  # Supports only one configuration

    def __init__(self):
        USBDevice.__init__(self)
        self.start_time = datetime.datetime.now()

    def generate_printer_report(self):
        pass

    def handle_data(self, usb_req):
        print hexdump(usb_req)

    def handle_unknown_control(self, control_req, usb_req):
        if control_req.bmRequestType == 0x81:
            if control_req.bRequest == 0x6:  # Get Descriptor
                print 'want descriptor'
        if control_req.bmRequestType == 0x21:  # Host Request
            if control_req.bRequest == 0x0a:  # set idle
                print 'Idle'
                # Idle
                pass
        print "control_req"
        print hexdump(control_req)
        print "usb_req"
        print hexdump(usb_req)


usb_Dev = USBPrinter()
usb_container = USBContainer()
usb_container.add_usb_device(usb_Dev)  # Supports only one device!
print "Starting Run"
usb_container.run()

# Run in cmd: usbip.exe -a 127.0.0.1 "1-1"
