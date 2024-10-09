# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Item:
    """DO NOT CHANGE THIS CLASS!!!"""
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class UpdateStrategy(ABC):
    @abstractmethod
    def update_quality(self, item):
        pass


class NormalItemStrategy(UpdateStrategy):
    def update_quality(self, item):
        item.sell_in -= 1
        if item.quality > 0:
            item.quality -= 1
            if item.sell_in < 0 and item.quality > 0:
                item.quality -= 1


class AgedBrieStrategy(UpdateStrategy):
    def update_quality(self, item):
        item.sell_in -= 1
        if item.quality < 50:
            item.quality += 1
            if item.sell_in < 0 and item.quality < 50:
                item.quality += 1


class BackstagePassStrategy(UpdateStrategy):
    def update_quality(self, item):
        item.sell_in -= 1
        if item.quality < 50:
            item.quality += 1
            if item.sell_in < 11 and item.quality < 50:
                item.quality += 1
            if item.sell_in < 6 and item.quality < 50:
                item.quality += 1
        if item.sell_in < 0:
            item.quality = 0


class SulfurasStrategy(UpdateStrategy):
    def update_quality(self, item):
        pass  # Sulfuras never changes


class ConjuredItemStrategy(UpdateStrategy):
    def update_quality(self, item):
        item.sell_in -= 1
        if item.quality > 0:
            item.quality -= 2
            if item.sell_in < 0 and item.quality > 0:
                item.quality -= 2
        item.quality = max(0, item.quality)  # Ensure quality doesn't go below 0


class GildedRose:
    def __init__(self, items: list[Item]):
        # DO NOT CHANGE THIS ATTRIBUTE!!!
        self.items = items
        self.strategies = {
            "Aged Brie": AgedBrieStrategy(),
            "Backstage passes to a TAFKAL80ETC concert": BackstagePassStrategy(),
            "Sulfuras, Hand of Ragnaros": SulfurasStrategy(),
            "Conjured": ConjuredItemStrategy()
        }

    def update_quality(self):
        for item in self.items:
            if item.name.startswith("Conjured"):
                strategy = self.strategies["Conjured"]
            else:
                strategy = self.strategies.get(item.name, NormalItemStrategy())
            strategy.update_quality(item)
            self._update_quality_bounds(item)

    def _update_quality_bounds(self, item):
        item.quality = max(0, min(item.quality, 50))
