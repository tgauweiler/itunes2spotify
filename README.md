# itunes2spotify
Migrate an iTunes playlist to Spotify.

`python itunes2spotify.py username playlist.xml`

*"I just don't understand why you're bothering. Your taste in music is so bad, I don't see why you wouldn't use Spotify as a chance for a clean slate." -- My wife*

iTunes has become Apple's middle finger to the world.

Bitter, I refuse to use Apple Music.

So Spotify!

Alas, Spotify has decided that their wall garden should not just be hard to
leave, but also hard to enter.  

They *removed* the ability to import iTunes playlists.  

Meaning, they did all the hard work of making it all work, then decided to
throw it out.

I assume they have enough money, as they made it hard for users to give it to them.

I saw they had an API which basically allowed of it.  Apple can
export playlists in XML.  I'd say awful XML, but that's redundant.  

Anyway, I thought a fun weekend project would be to play with Python, glue it
 all together & be free of iTunes.  

So here we are.

That said, this is very brittle.  It's a hack.  There's minimal error checking.
There's no unit tests.  It's hack hack hack.  I should be ashamed, but
let's be honest, I've done worse.  And so have you.

I have no idea if it will work for you.  It probably will.  If you write
something better let me know & I'll point people there.
