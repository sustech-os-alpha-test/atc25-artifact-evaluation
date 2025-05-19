// SPDX-License-Identifier: MPL-2.0

use crate::mm::PAGE_SIZE;

pub struct InterruptEntryCache(pub u128);

impl InterruptEntryCache {
    const INVALIDATION_TYPE: u128 = 4;

    pub fn global_invalidation() -> Self {
        Self(Self::INVALIDATION_TYPE)
    }
}

pub struct IotlbInvalidation(pub u128);

impl IotlbInvalidation {
    const INVALIDATION_TYPE: u128 = 2;

    pub fn global_invalidation() -> Self {
        Self(Self::INVALIDATION_TYPE | 0b01_0000)
    }

    pub fn with_address(daddr: u64) -> Self {
        Self(Self::INVALIDATION_TYPE | (((daddr & 0xFFFF_FFFF_FFFF_F000) as u128) << 64)  | 0b11_0000)
    }
}

pub struct DevicetlbInvalidation(pub u128);

impl DevicetlbInvalidation {
    const INVALIDATION_TYPE: u128 = 3;

    pub fn global_invalidation() -> Self {
        Self(Self::INVALIDATION_TYPE)
    }

    pub fn with_address(daddr: u64) -> Self {
        Self(Self::INVALIDATION_TYPE | (((daddr & 0xFFFF_FFFF_FFFF_F000) as u128) << 64)  | 0b11_0000)
    }
}


pub struct InvalidationWait(pub u128);

impl InvalidationWait {
    const INVALIDATION_TYPE: u128 = 5;

    pub fn with_interrupt_flag() -> Self {
        Self(Self::INVALIDATION_TYPE | 0x10)
    }
}
