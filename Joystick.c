/*
Nintendo Switch Fightstick - Proof-of-Concept

Based on the LUFA library's Low-Level Joystick Demo
(C) Dean Camera
Based on the HORI's Pokken Tournament Pro Pad design
(C) HORI

This project implements a modified version of HORI's Pokken Tournament Pro Pad
USB descriptors to allow for the creation of custom controllers for the
Nintendo Switch. This also works to a limited degree on the PS3.

Since System Update v3.0.0, the Nintendo Switch recognizes the Pokken
Tournament Pro Pad as a Pro Controller. Physical design limitations prevent
the Pokken Controller from functioning at the same level as the Pro
Controller. However, by default most of the descriptors are there, with the
exception of Home and Capture. Descriptor modification allows us to unlock
these buttons for our use.
*/

/** \file
*
*  Main source file for the Joystick demo. This file contains the main tasks of the demo and
*  is responsible for the initial application hardware configuration.
*/

#include <LUFA/Drivers/Peripheral/Serial.h>
#include "Joystick.h"

uint8_t target = RELEASE;
uint16_t buttons;

uint8_t HAT2 = 0;
int LX2 = 0;     // Left  Stick X
int LY2 = 0;     // Left  Stick Y
int RX2 = 0;     // Right Stick X
int RY2 = 0;     // Right Stick Y


void parseLine(char* line) {

	char btns[16];


	sscanf(line, "%s %hhu %hhu %hhu %hhu", btns, &LX2, &LY2, &RX2, &RY2);


	buttons = SWITCH_RELEASE;
	HAT2 = 0;

	switch (btns[0]) {
	case '0':
		HAT2 = HAT_TOP;
		break;
	case '1':
		HAT2 = HAT_TOP_RIGHT;
		break;
	case '2':
		HAT2 = HAT_RIGHT;
		break;
	case '3':
		HAT2 = HAT_BOTTOM_RIGHT;
		break;
	case '4':
		HAT2 = HAT_BOTTOM;
		break;
	case '5':
		HAT2 = HAT_BOTTOM_LEFT;
		break;
	case '6':
		HAT2 = HAT_LEFT;
		break;
	case '7':
		HAT2 = HAT_TOP_LEFT;
		break;
	case '8':
		HAT2 = HAT_CENTER;
		break;
	default:
		break;
	}
	
	if (btns[1] == '1') {
		buttons |= SWITCH_LCLICK;
	}
	if (btns[2] == '1') {
		buttons |= SWITCH_L;
	}
	if (btns[3] == '1') {
		buttons = SWITCH_ZL;
	}
	if (btns[4] == '1') {
		buttons |= SWITCH_SELECT;
	}
	if (btns[5] == '1') {
		buttons |= SWITCH_CAPTURE;
	}
	if (btns[6] == '1') {
		buttons |= SWITCH_A;
	}
	if (btns[7] == '1') {
		buttons |= SWITCH_B;
	}
	if (btns[8] == '1') {
		buttons |= SWITCH_X;
	}
	if (btns[9] == '1') {
		buttons |= SWITCH_Y;
	}
	if (btns[10] == '1') {
		buttons |= SWITCH_RCLICK;
	}
	if (btns[11] == '1') {
		buttons |= SWITCH_R;
	}
	if (btns[12] == '1') {
		buttons |= SWITCH_ZR;
	}
	if (btns[13] == '1') {
		buttons |= SWITCH_START;
	}
	if (btns[14] == '1') {
		buttons |= SWITCH_HOME;
	}
}

#define MAX_BUFFER 32
char b[MAX_BUFFER];
uint8_t l = 0;
ISR(USART1_RX_vect) {
	char c = fgetc(stdin);
	if (Serial_IsSendReady()) {
		printf("%c", c);
	}
	if (c == '\r') {
		parseLine(b);
		l = 0;
		memset(b, 0, sizeof(b));
	} else if (c != '\n' && l < MAX_BUFFER) {
		b[l++] = c;
	}
}

// Main entry point.
int main(void) {
	Serial_Init(9600, false);
	Serial_CreateStream(NULL);

	sei();
	UCSR1B |= (1 << RXCIE1);

	// We'll start by performing hardware and peripheral setup.
	SetupHardware();
	// We'll then enable global interrupts for our use.
	GlobalInterruptEnable();
	// Once that's done, we'll enter an infinite loop.
	for (;;)
	{
		// We need to run our task to process and deliver data for our IN and OUT endpoints.
		HID_Task();
		// We also need to run the main USB management task.
		USB_USBTask();
	}
}

// Configures hardware and peripherals, such as the USB peripherals.
void SetupHardware(void) {
	// We need to disable watchdog if enabled by bootloader/fuses.
	MCUSR &= ~(1 << WDRF);
	wdt_disable();

	// We need to disable clock division before initializing the USB hardware.
	clock_prescale_set(clock_div_1);
	// We can then initialize our hardware and peripherals, including the USB stack.

	// The USB stack should be initialized last.
	USB_Init();
}

// Fired to indicate that the device is enumerating.
void EVENT_USB_Device_Connect(void) {
	// We can indicate that we're enumerating here (via status LEDs, sound, etc.).
}

// Fired to indicate that the device is no longer connected to a host.
void EVENT_USB_Device_Disconnect(void) {
	// We can indicate that our device is not ready (via status LEDs, sound, etc.).
}

// Fired when the host set the current configuration of the USB device after enumeration.
void EVENT_USB_Device_ConfigurationChanged(void) {
	bool ConfigSuccess = true;

	// We setup the HID report endpoints.
	ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_OUT_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);
	ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_IN_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);

	// We can read ConfigSuccess to indicate a success or failure at this point.
}

// Process control requests sent to the device from the USB host.
void EVENT_USB_Device_ControlRequest(void) {
	// We can handle two control requests: a GetReport and a SetReport.
	switch (USB_ControlRequest.bRequest)
	{
		// GetReport is a request for data from the device.
	case HID_REQ_GetReport:
		if (USB_ControlRequest.bmRequestType == (REQDIR_DEVICETOHOST | REQTYPE_CLASS | REQREC_INTERFACE))
		{
			// We'll create an empty report.
			USB_JoystickReport_Input_t JoystickInputData;
			// We'll then populate this report with what we want to send to the host.
			GetNextReport(&JoystickInputData);
			// Since this is a control endpoint, we need to clear up the SETUP packet on this endpoint.
			Endpoint_ClearSETUP();
			// Once populated, we can output this data to the host. We do this by first writing the data to the control stream.
			Endpoint_Write_Control_Stream_LE(&JoystickInputData, sizeof(JoystickInputData));
			// We then acknowledge an OUT packet on this endpoint.
			Endpoint_ClearOUT();
		}

		break;
	case HID_REQ_SetReport:
		if (USB_ControlRequest.bmRequestType == (REQDIR_HOSTTODEVICE | REQTYPE_CLASS | REQREC_INTERFACE))
		{
			// We'll create a place to store our data received from the host.
			USB_JoystickReport_Output_t JoystickOutputData;
			// Since this is a control endpoint, we need to clear up the SETUP packet on this endpoint.
			Endpoint_ClearSETUP();
			// With our report available, we read data from the control stream.
			Endpoint_Read_Control_Stream_LE(&JoystickOutputData, sizeof(JoystickOutputData));
			// We then send an IN packet on this endpoint.
			Endpoint_ClearIN();
		}

		break;
	}
}

// Process and deliver data from IN and OUT endpoints.
void HID_Task(void) {
	// If the device isn't connected and properly configured, we can't do anything here.
	if (USB_DeviceState != DEVICE_STATE_Configured)
		return;

	// We'll start with the OUT endpoint.
	Endpoint_SelectEndpoint(JOYSTICK_OUT_EPADDR);
	// We'll check to see if we received something on the OUT endpoint.
	if (Endpoint_IsOUTReceived())
	{
		// If we did, and the packet has data, we'll react to it.
		if (Endpoint_IsReadWriteAllowed())
		{
			// We'll create a place to store our data received from the host.
			USB_JoystickReport_Output_t JoystickOutputData;
			// We'll then take in that data, setting it up in our storage.
			Endpoint_Read_Stream_LE(&JoystickOutputData, sizeof(JoystickOutputData), NULL);
			// At this point, we can react to this data.
			// However, since we're not doing anything with this data, we abandon it.
		}
		// Regardless of whether we reacted to the data, we acknowledge an OUT packet on this endpoint.
		Endpoint_ClearOUT();
	}

	// We'll then move on to the IN endpoint.
	Endpoint_SelectEndpoint(JOYSTICK_IN_EPADDR);
	// We first check to see if the host is ready to accept data.
	if (Endpoint_IsINReady())
	{
		// We'll create an empty report.
		USB_JoystickReport_Input_t JoystickInputData;
		// We'll then populate this report with what we want to send to the host.
		GetNextReport(&JoystickInputData);
		// Once populated, we can output this data to the host. We do this by first writing the data to the control stream.
		Endpoint_Write_Stream_LE(&JoystickInputData, sizeof(JoystickInputData), NULL);
		// We then send an IN packet on this endpoint.
		Endpoint_ClearIN();

		/* Clear the report data afterwards */
		// memset(&JoystickInputData, 0, sizeof(JoystickInputData));
	}
}

// Prepare the next report for the host.
void GetNextReport(USB_JoystickReport_Input_t* const ReportData) {
	/* Clear the report contents */
	memset(ReportData, 0, sizeof(USB_JoystickReport_Input_t));
	ReportData->LX = STICK_CENTER;
	ReportData->LY = STICK_CENTER;
	ReportData->RX = STICK_CENTER;
	ReportData->RY = STICK_CENTER;
	ReportData->HAT = HAT_CENTER;
	ReportData->Button = SWITCH_RELEASE;


	ReportData->Button |= buttons;
	ReportData->HAT = HAT2;

	ReportData->LX = LX2;
	ReportData->LY = LY2;
	ReportData->RX = RX2;
	ReportData->RY = RY2;
}
// vim: noexpandtab
