import asyncio
from state_checker import *
from ble_base_test import BleBaseTest, BleBaseTestArgs
from base_test import BaseTestException

class TestDimmerBoot(BleBaseTest):
	@staticmethod
	def get_name() -> str:
		return __class__.__name__

	@staticmethod
	def get_description() -> str:
		return "Test dimmer boot."

	async def _run_ble(self):
		await self.setup()

		# ====================================================================
		await self.dimmed_cold_boot()

		self.logger.info("Checking if setting a dimmed value, while dimmer is not ready, has no effect.")
		await self.connect()
		await self.core.control.setDimmer(10)
		await SwitchStateChecker(self.state_checker_args, 0, True).check()
		await DimmerReadyChecker(self.state_checker_args, False).check()
		await self.core.disconnect()
		await DimmerReadyChecker(self.state_checker_args, False).check()  # Also check service data.

		self.logger.info("Checking if changing the dim value, while dimmer is not ready, has no effect either.")
		await self.connect()
		await self.core.control.setDimmer(15)
		await SwitchStateChecker(self.state_checker_args, 0, True).check()

		self.logger.info("Checking if dimmed value will not be set once the dimmer is ready.")
		await DimmerReadyChecker(self.state_checker_args, True).wait_for_state_match()
		await SwitchStateChecker(self.state_checker_args, 0, True).check()

		# ====================================================================
		await self.dimmed_cold_boot()
		self.logger.info("Checking if stored dimmed value is not set once the dimmer is ready after boot.")
		await DimmerReadyChecker(self.state_checker_args, True).wait_for_state_match()
		await SwitchStateChecker(self.state_checker_args, 0, True).check()

		# ====================================================================
		await self.connect()
		hardwareVersion = await self.core.debug.getHardwareVersion()
		can_try_dimmer_on_cold_boot = False
		if hardwareVersion.startswith("10106"):
			self.logger.info("Crownstone is a builtin one.")
			can_try_dimmer_on_cold_boot = True

		if not can_try_dimmer_on_cold_boot:
			raise Exception("Can't check if you can use dimmer immediately after cold boot, with sufficient large load.")

		await DimmerReadyChecker(self.state_checker_args, True).wait_for_state_match()
		self.logger.info("Checking if you can use dimmer immediately after cold boot, with sufficient large load.")
		await self.set_switch(False, 100, True, False)

		load_min = 10
		load_max = 30
		self.user_action_request(f"Plug in a dimmable load of {load_min}W - {load_max}W.")
		await PowerUsageChecker(self.state_checker_args, load_min, load_max).check()

		self.logger.info("Waiting for switch state to be stored.")
		await asyncio.sleep(10)

		await self.cold_boot()

		self.logger.info("Checking if dimmer stays turned on.")
		for i in range(0, 20):
			await SwitchStateChecker(self.state_checker_args, 100, False).check()
			await asyncio.sleep(3)

		# ====================================================================
		await self.connect()
		hardwareVersion = await self.core.debug.getHardwareVersion()
		can_use_dimmer_on_warm_boot = False
		if hardwareVersion.startswith("101060001"):
			self.logger.info("Crownstone is a builtin one v25.")
			can_use_dimmer_on_warm_boot = True

		if not can_use_dimmer_on_warm_boot:
			raise Exception("Can't check if you can use dimmer immediately after cold boot, with sufficient large load.")


		await DimmerReadyChecker(self.state_checker_args, True).wait_for_state_match()
		self.logger.info("Checking if you can use dimmer immediately after warm boot.")
		await self.set_switch(False, 10, True, False)

		self.user_action_request(f"Plug out any load.")
		load_min = -10
		load_max = 1
		await PowerUsageChecker(self.state_checker_args, load_min, load_max).check()

		self.logger.info("Waiting for switch state to be stored.")
		await asyncio.sleep(10)

		self.logger.info("Reboot")
		await self.connect()
		await self.core.control.reset()

		self.logger.info("Checking if dimmer stays turned on.")
		for i in range(0, 20):
			await SwitchStateChecker(self.state_checker_args, 10, False).check()
			await asyncio.sleep(3)



	async def dimmed_cold_boot(self):
		"""
		Cold boot the crownstone, with dimming enabled and a stored dimmed value.
		Returns before dimmer is ready, with relay on instead of dimmer.
		"""
		self.logger.info("Checking if you can't use dimmer immediately after boot.")
		await DimmerReadyChecker(self.state_checker_args, True).wait_for_state_match()
		await self.set_switch(False, 100, True, False)

		load_min = 0
		load_max = 20
		self.user_action_request(f"Plug in a dimmable load of {load_min}W - {load_max}W.")
		await PowerUsageChecker(self.state_checker_args, load_min, load_max).check()

		await self.set_switch(False, 10)
		self.logger.info("Waiting for switch state to be stored.")
		await asyncio.sleep(10)

		await self.cold_boot()

		self.logger.info("Waiting for power check to be finished.")
		await asyncio.sleep(5)

		self.logger.info("Checking if relay was turned on instead of dimmer.")
		await SwitchStateChecker(self.state_checker_args, 0, True).check()

	async def cold_boot(self):
		self.user_action_request(f"Plug out the crownstone.")
		await asyncio.sleep(1)
		self.user_action_request(f"Plug in the crownstone.")
