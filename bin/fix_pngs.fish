#!/bin/sh

ls ld40_setup/resources/**/*.png | while read -l line;
  pngcrush -ow -rem allb -reduce $line
end
