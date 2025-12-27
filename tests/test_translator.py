#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for TranslationSystem"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from translator import TranslationSystem


def test_init_with_locale():
    """Test initialization with locale"""
    ts = TranslationSystem("de_DE")
    assert ts.get_locale() == "de_DE"


def test_init_without_locale():
    """Test initialization without locale"""
    ts = TranslationSystem()
    assert ts.get_locale() is None


def test_set_locale():
    """Test changing locale"""
    ts = TranslationSystem()
    ts.set_locale("de_DE")
    assert ts.get_locale() == "de_DE"


def test_tr_basic():
    """Test basic translation"""
    ts = TranslationSystem("de_DE")
    result = ts.tr("Hello")
    assert isinstance(result, str)


def test_tr_with_fontsize():
    """Test tr() with fontsize parameter"""
    ts = TranslationSystem("de_DE")
    result = ts.tr("Settings", 16)
    assert isinstance(result, str)


def test_tr_size():
    """Test tr_size() returns valid size"""
    ts = TranslationSystem("de_DE")
    ts.tr("Settings", 20)
    size = ts.tr_size()
    assert size > 0


def test_placeholder_extraction():
    """Test placeholder extraction"""
    ts = TranslationSystem()
    placeholders = ts.extract_placeholders("Hello {name}, you have {count} messages")
    assert len(placeholders) == 2
    assert "{name}" in placeholders
    assert "{count}" in placeholders


def test_alias():
    """Test _ alias works"""
    ts = TranslationSystem("de_DE")
    _ = ts.tr
    result = _("Hello")
    assert isinstance(result, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
