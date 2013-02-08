#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Moodle bundle for Sublime Text

Copyright (c) 2012 Frédéric Massart - FMCorz.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

http://github.com/FMCorz/SublimeMoodle
"""

import sublime
import sublime_plugin
import re
import os


class MoodleWriteTestingInstructionsCommand(sublime_plugin.WindowCommand):

    _syntax = "Syntaxes/Testing Instructions.tmLanguage"
    _template = """*Test pre-requisites*

- CURSOR

*Test steps*

# 
"""

    def run(self):
        view = self.window.new_file()
        edit = view.begin_edit()

        here = os.path.dirname(os.path.realpath(__file__))
        syntax = os.path.join(here, self._syntax)
        if os.path.isfile(syntax):
            view.set_syntax_file(syntax)

        view.insert(edit, 0, self._template)
        region = view.find(r'CURSOR', 0)
        view.erase(edit, region)
        view.sel().clear()
        view.sel().add(sublime.Region(region.begin()))
        view.end_edit(edit)

    def description(self):
        return
        """
        Opens a new window with a template for writing testing instructions.
        """.strip()


class MoodleTestingIdent(sublime_plugin.TextCommand):

    def run(self, edit, mode='after', key='-'):
        for region in self.view.sel():
            if mode == 'after':
                line = self.view.line(region)
                lineContent = self.view.substr(line)
                ident = re.match(r'((#|-)+)\s*$', lineContent)
                if ident != None:
                    chars = ident.group(1)
                    if len(chars) > 1:
                        self.view.replace(edit, line, chars[:-1] + ' ')
                    else:
                        self.view.replace(edit, line, '\n')

            elif mode == 'extend':
                line = self.view.line(region)
                lineContent = self.view.substr(line).strip()
                if lineContent == '':
                    # Empty lines would create a selection, insert prevents that.
                    self.view.insert(edit, line.begin(), key + ' ')
                else:
                    self.view.replace(edit, line, lineContent + key + ' ')

            elif mode == 'ident' or mode == 'unident':
                regions = self.view.lines(region)
                regions.reverse()
                for line in regions:
                    if mode == 'ident':
                        char = '- '
                        if re.match(r'[#-]', self.view.substr(line.begin())):
                            char = '-'
                        self.view.insert(edit, line.begin(), char)

                    elif mode == 'unident':
                        if re.match(r'[#-]', self.view.substr(line.begin())):
                            self.view.erase(edit, sublime.Region(line.begin(), line.begin() + 1))
                            while re.match(r' ', self.view.substr(line.begin())):
                                self.view.erase(edit, sublime.Region(line.begin(), line.begin() + 1))

