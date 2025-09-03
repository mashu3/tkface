"""Tests for tkface.lang.lang module."""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest
from tkinter import TclError

import tkface.lang.lang


class TestLanguageManager:
    """Test LanguageManager class."""

    def test_init(self, lang_manager):
        """Test LanguageManager initialization."""
        assert lang_manager.current_lang == "en"
        assert lang_manager.user_dicts == {}
        assert lang_manager.msgcat_loaded == set()

    def test_register(self, mock_root, lang_manager, sample_translations):
        """Test register method."""
        test_dict = sample_translations["ja"]
        lang_manager.register("ja", test_dict, mock_root)
        
        assert "ja" in lang_manager.user_dicts
        assert lang_manager.user_dicts["ja"] == test_dict

    def test_register_multiple_languages(self, mock_root, lang_manager, sample_translations):
        """Test registering multiple languages."""
        ja_dict = sample_translations["ja"]
        en_dict = sample_translations["en"]
        
        lang_manager.register("ja", ja_dict, mock_root)
        lang_manager.register("en", en_dict, mock_root)
        
        assert "ja" in lang_manager.user_dicts
        assert "en" in lang_manager.user_dicts
        assert lang_manager.user_dicts["ja"]["hello"] == "こんにちは"
        assert lang_manager.user_dicts["en"]["hello"] == "Hello"

    def test_register_update_existing(self, mock_root, lang_manager, sample_translations):
        """Test updating existing language dictionary."""
        initial_dict = sample_translations["en"]
        lang_manager.register("en", initial_dict, mock_root)
        
        update_dict = {"goodbye": "Goodbye"}
        lang_manager.register("en", update_dict, mock_root)
        
        assert lang_manager.user_dicts["en"]["hello"] == "Hello"
        assert lang_manager.user_dicts["en"]["goodbye"] == "Goodbye"

    def test_determine_language_auto_success(self, mock_root_with_locale, lang_manager):
        """Test _determine_language with 'auto' and successful locale detection."""
        mock_root_with_locale.tk.call.return_value = "ja_JP"
        
        result = lang_manager._determine_language("auto", mock_root_with_locale)
        assert result == "ja_JP"

    def test_determine_language_auto_fallback(self, mock_root_tcl_error, lang_manager):
        """Test _determine_language with 'auto' and fallback to 'en'."""
        result = lang_manager._determine_language("auto", mock_root_tcl_error)
        assert result == "en"

    def test_determine_language_direct(self, mock_root, lang_manager):
        """Test _determine_language with direct language code."""
        result = lang_manager._determine_language("fr", mock_root)
        assert result == "fr"

    def test_load_tk_msgcat_success_full(self, mock_root_with_locale, lang_manager):
        """Test _load_tk_msgcat with full language code success."""
        with patch('os.path.exists', return_value=True):
            lang_manager._load_tk_msgcat("ja_JP", mock_root_with_locale)
            
            mock_root_with_locale.tk.call.assert_called()
            assert "ja_JP" in lang_manager.msgcat_loaded

    def test_load_tk_msgcat_success_short(self, mock_root_with_locale, lang_manager):
        """Test _load_tk_msgcat with short language code success."""
        with patch('os.path.exists', side_effect=[False, True]):  # Full path doesn't exist, short does
            lang_manager._load_tk_msgcat("ja_JP", mock_root_with_locale)
            
            mock_root_with_locale.tk.call.assert_called()
            assert "ja_JP" in lang_manager.msgcat_loaded

    def test_load_tk_msgcat_failure(self, mock_root_with_locale, lang_manager):
        """Test _load_tk_msgcat with failure."""
        mock_root_with_locale.tk.call.side_effect = TclError("File not found")
        
        # Should not raise exception
        lang_manager._load_tk_msgcat("ja_JP", mock_root_with_locale)
        
        assert "ja_JP" not in lang_manager.msgcat_loaded

    def test_load_tk_msgcat_tcl_error(self, mock_root_tcl_error, lang_manager):
        """Test _load_tk_msgcat with TclError during call."""
        with patch('os.path.exists', return_value=True):
            # Should not raise exception
            lang_manager._load_tk_msgcat("ja_JP", mock_root_tcl_error)
            
            assert "ja_JP" not in lang_manager.msgcat_loaded

    def test_parse_msg_file(self, mock_root, lang_manager):
        """Test _parse_msg_file method."""
        # Create temporary message file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.msg', delete=False) as f:
            f.write("hello{こんにちは}\n")
            f.write("goodbye{さようなら}\n")
            f.write("# This is a comment\n")
            f.write("  \n")  # Empty line
            temp_file = f.name
        
        try:
            lang_manager._parse_msg_file(temp_file, "ja", mock_root)
            
            assert "ja" in lang_manager.user_dicts
            assert lang_manager.user_dicts["ja"]["hello"] == "こんにちは"
            assert lang_manager.user_dicts["ja"]["goodbye"] == "さようなら"
        finally:
            os.unlink(temp_file)

    def test_load_custom_msgcat_success_full(self, mock_root_with_locale, lang_manager):
        """Test _load_custom_msgcat with full language code success."""
        with patch('os.path.exists', return_value=True), \
             patch.object(tkface.lang.lang.LanguageManager, '_parse_msg_file') as mock_parse:
            
            lang_manager._load_custom_msgcat("ja_JP", mock_root_with_locale)
            
            mock_parse.assert_called()
            mock_root_with_locale.tk.call.assert_called()
            assert "ja_JP" in lang_manager.msgcat_loaded

    def test_load_custom_msgcat_success_short(self, mock_root_with_locale, lang_manager):
        """Test _load_custom_msgcat with short language code success."""
        with patch('os.path.exists', side_effect=[False, True]):  # Full path doesn't exist, short does
            lang_manager._load_custom_msgcat("ja_JP", mock_root_with_locale)
            
            mock_root_with_locale.tk.call.assert_called()
            assert "ja" in lang_manager.msgcat_loaded

    def test_load_custom_msgcat_failure(self, mock_root_with_locale, lang_manager):
        """Test _load_custom_msgcat with failure."""
        with patch('os.path.exists', return_value=False):
            # Should not raise exception
            lang_manager._load_custom_msgcat("ja_JP", mock_root_with_locale)
            
            assert "ja_JP" not in lang_manager.msgcat_loaded

    def test_load_custom_msgcat_parse_error(self, mock_root_with_locale, lang_manager):
        """Test _load_custom_msgcat with parse error."""
        with patch('os.path.exists', return_value=True), \
             patch.object(tkface.lang.lang.LanguageManager, '_parse_msg_file') as mock_parse:
            
            mock_parse.side_effect = TclError("Parse error")
            
            # Should not raise exception
            lang_manager._load_custom_msgcat("ja_JP", mock_root_with_locale)
            
            assert "ja_JP" not in lang_manager.msgcat_loaded

    def test_load_custom_msgcat_file_error(self, mock_root_with_locale, lang_manager):
        """Test _load_custom_msgcat with file error."""
        with patch('os.path.exists', return_value=True), \
             patch.object(tkface.lang.lang.LanguageManager, '_parse_msg_file') as mock_parse:
            
            mock_parse.side_effect = OSError("File not found")
            
            # Should not raise exception
            lang_manager._load_custom_msgcat("ja_JP", mock_root_with_locale)
            
            assert "ja_JP" not in lang_manager.msgcat_loaded

    def test_set_final_locale_success(self, mock_root, lang_manager):
        """Test _set_final_locale with success."""
        lang_manager._set_final_locale("ja", mock_root)
        mock_root.tk.call.assert_called_with("msgcat::mclocale", "ja")

    def test_set_final_locale_failure(self, mock_root_tcl_error, lang_manager):
        """Test _set_final_locale with failure."""
        # Should not raise exception
        lang_manager._set_final_locale("ja", mock_root_tcl_error)

    def test_set_language(self, mock_root, lang_manager):
        """Test set method."""
        with patch.object(tkface.lang.lang.LanguageManager, '_load_tk_msgcat') as mock_load_tk, \
             patch.object(tkface.lang.lang.LanguageManager, '_load_custom_msgcat') as mock_load_custom, \
             patch.object(tkface.lang.lang.LanguageManager, '_set_final_locale') as mock_set_final:
            
            lang_manager.set("ja", mock_root)
            
            assert lang_manager.current_lang == "ja"
            mock_load_tk.assert_called_with("ja", mock_root)
            mock_load_custom.assert_called_with("ja", mock_root)
            mock_set_final.assert_called_with("ja", mock_root)

    def test_set_language_auto(self, mock_root_with_locale, lang_manager):
        """Test set method with 'auto' language."""
        with patch.object(tkface.lang.lang.LanguageManager, '_determine_language') as mock_determine, \
             patch.object(tkface.lang.lang.LanguageManager, '_load_tk_msgcat') as mock_load_tk, \
             patch.object(tkface.lang.lang.LanguageManager, '_load_custom_msgcat') as mock_load_custom, \
             patch.object(tkface.lang.lang.LanguageManager, '_set_final_locale') as mock_set_final:
            
            mock_determine.return_value = "ja"
            
            lang_manager.set("auto", mock_root_with_locale)
            
            mock_determine.assert_called_with("auto", mock_root_with_locale)
            assert lang_manager.current_lang == "ja"

    def test_get_with_user_dict(self, mock_root, lang_manager):
        """Test get method with user dictionary."""
        test_dict = {"hello": "こんにちは"}
        lang_manager.user_dicts["ja"] = test_dict
        lang_manager.current_lang = "ja"
        
        result = lang_manager.get("hello", mock_root, "ja")
        assert result == "こんにちは"

    def test_get_with_msgcat_success(self, mock_root, lang_manager):
        """Test get method with msgcat success."""
        mock_root.tk.call.side_effect = [
            "en",           # Get original locale
            "ja",           # Set locale to ja
            "こんにちは",    # Get translation
            "en"            # Restore original locale
        ]
        
        result = lang_manager.get("hello", mock_root, "ja")
        
        assert result == "こんにちは"

    def test_get_with_msgcat_failure_fallback_to_english(self, mock_root, lang_manager):
        """Test get method with msgcat failure, fallback to English."""
        mock_root.tk.call.side_effect = [
            TclError("Translation not found"),  # Japanese
            "en",  # Set English locale
            "Hello",  # English translation
            "ja"   # Restore Japanese locale
        ]
        
        result = lang_manager.get("hello", mock_root, "ja")
        
        assert result == "Hello"

    def test_get_with_msgcat_failure_return_key(self, mock_root, lang_manager):
        """Test get method with msgcat failure, return key as fallback."""
        mock_root.tk.call.side_effect = [
            TclError("Translation not found"),  # Japanese
            TclError("English translation not found")  # English
        ]
        
        result = lang_manager.get("hello", mock_root, "ja")
        
        assert result == "hello"

    def test_get_without_root_no_default(self):
        """Test get method without root and no default root."""
        with patch('tkinter._default_root', None):
            lang_manager = tkface.lang.lang.LanguageManager()
            with pytest.raises(RuntimeError):
                lang_manager.get("hello")

    def test_get_without_root_with_default(self, mock_root):
        """Test get method without root but with default root."""
        mock_root.tk = Mock()
        mock_root.tk.call = Mock()
        
        with patch('tkinter._default_root', mock_root):
            test_dict = {"hello": "こんにちは"}
            lang_manager = tkface.lang.lang.LanguageManager()
            lang_manager.user_dicts["ja"] = test_dict
            lang_manager.current_lang = "ja"
            
            result = lang_manager.get("hello", language="ja")
            assert result == "こんにちは"

    def test_mc_alias(self, mock_root, lang_manager):
        """Test mc alias for get method."""
        test_dict = {"hello": "こんにちは"}
        lang_manager.user_dicts["ja"] = test_dict
        lang_manager.current_lang = "ja"
        
        result = lang_manager.mc("hello", mock_root, "ja")
        assert result == "こんにちは"

    def test_available(self, lang_manager):
        """Test available method."""
        lang_manager.user_dicts["ja"] = {}
        lang_manager.user_dicts["fr"] = {}
        lang_manager.msgcat_loaded.add("de")
        
        available = lang_manager.available()
        
        assert "ja" in available
        assert "fr" in available
        assert "de" in available
        assert "en" in available
        assert available == sorted(["de", "en", "fr", "ja"])

    def test_available_empty(self, lang_manager):
        """Test available method with no languages."""
        available = lang_manager.available()
        assert available == ["en"]

    def test_load_msg_success(self, mock_root, lang_manager):
        """Test load_msg method with success."""
        with patch('os.path.abspath', return_value="/absolute/path/to/file.msg"):
            result = lang_manager.load_msg("ja", "/path/to/file.msg", mock_root)
            
            assert result is True
            mock_root.tk.call.assert_called_with("msgcat::mcload", "/absolute/path/to/file.msg")
            assert "ja" in lang_manager.msgcat_loaded

    def test_load_msg_failure(self, mock_root, lang_manager):
        """Test load_msg method with failure."""
        mock_root.tk.call.side_effect = TclError("File not found")
        
        with patch('os.path.abspath', return_value="/absolute/path/to/file.msg"):
            result = lang_manager.load_msg("ja", "/path/to/file.msg", mock_root)
            
            assert result is False
            assert "ja" not in lang_manager.msgcat_loaded

    def test_clear(self, lang_manager):
        """Test clear method."""
        lang_manager.user_dicts["ja"] = {"hello": "こんにちは"}
        lang_manager.user_dicts["fr"] = {"hello": "Bonjour"}
        
        lang_manager.clear("ja")
        
        assert "ja" not in lang_manager.user_dicts
        assert "fr" in lang_manager.user_dicts

    def test_clear_nonexistent(self, lang_manager):
        """Test clear method with nonexistent language."""
        initial_dicts = lang_manager.user_dicts.copy()
        
        lang_manager.clear("nonexistent")
        
        assert lang_manager.user_dicts == initial_dicts

    def test_current(self, lang_manager):
        """Test current method."""
        lang_manager.current_lang = "ja"
        assert lang_manager.current() == "ja"

    def test_get_dict(self, lang_manager):
        """Test get_dict method."""
        test_dict = {"hello": "こんにちは"}
        lang_manager.user_dicts["ja"] = test_dict
        
        result = lang_manager.get_dict("ja")
        assert result == test_dict

    def test_get_dict_nonexistent(self, lang_manager):
        """Test get_dict method with nonexistent language."""
        result = lang_manager.get_dict("nonexistent")
        assert result == {}


class TestLanguageManagerIntegration:
    """Integration tests for LanguageManager with real Tkinter root."""

    @pytest.fixture(autouse=True)
    def setup(self, root):
        """Set up test with real Tkinter root."""
        self.root = root
        self.lang_manager = tkface.lang.lang.LanguageManager()

    def test_register_with_real_root(self):
        """Test register method with real Tkinter root."""
        test_dict = {"hello": "こんにちは", "goodbye": "さようなら"}
        self.lang_manager.register("ja", test_dict, self.root)
        
        assert "ja" in self.lang_manager.user_dicts
        assert self.lang_manager.user_dicts["ja"] == test_dict

    def test_set_language_with_real_root(self):
        """Test set method with real Tkinter root."""
        # This test may fail if msgcat is not available, but should not crash
        try:
            self.lang_manager.set("en", self.root)
            assert self.lang_manager.current_lang == "en"
        except TclError:
            # Skip if msgcat is not available
            pytest.skip("msgcat not available in this Tkinter installation")

    def test_get_with_real_root(self):
        """Test get method with real Tkinter root."""
        test_dict = {"hello": "こんにちは"}
        self.lang_manager.user_dicts["ja"] = test_dict
        self.lang_manager.current_lang = "ja"
        
        result = self.lang_manager.get("hello", self.root, "ja")
        assert result == "こんにちは"
