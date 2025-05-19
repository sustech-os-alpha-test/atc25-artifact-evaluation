// SPDX-License-Identifier: MPL-2.0

use core::mem::size_of;

use crate::{
    mm::{FrameAllocOptions, Segment, VmIo, PAGE_SIZE},
    prelude::Paddr,
};

pub struct Queue {
    segment: Segment<()>,
    queue_size: usize,
    tail: usize,
}

impl Queue {
    pub fn append_descriptor(&mut self, descriptor: u128) {
        // if self.tail == self.queue_size - 1 {
        //     self.tail = 0;
        // }
        self.segment
            .write_val((self.tail % (self.queue_size)) * size_of::<u128>(), &descriptor)
            .unwrap();
        self.tail += 1;
    }

    pub fn tail(&self) -> usize {
        self.tail % (self.queue_size)
    }

    pub fn size(&self) -> usize {
        self.queue_size
    }

    pub(crate) fn base_paddr(&self) -> Paddr {
        self.segment.start_paddr()
    }

    pub(super) fn new() -> Self {
        const DEFAULT_PAGES: usize = 1;
        let segment = FrameAllocOptions::new()
            .alloc_segment(DEFAULT_PAGES)
            .unwrap();
        Self {
            segment,
            queue_size: (DEFAULT_PAGES * PAGE_SIZE) / size_of::<u128>(),
            tail: 0,
        }
    }
}
