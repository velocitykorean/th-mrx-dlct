import os, sys, json, time, requests, re
import config

# Pre-crafted master curriculum for The Marxian Dialectic channel (Karl Marx philosophical & political-economic masterworks)
MARX_CURRICULUM = [
    {
        "id": "ep_1",
        "topic": "The Riddle of Alienation: How Modern Work Estranges Us from Our Humanity",
        "focus": "A deep philosophical exploration of the 1844 Economic and Philosophic Manuscripts: how wage labor separates human beings from the product of their toil, from nature, from their species-essence (Gattungswesen), and from each other.",
        "thumbnail_title_1": "ALIENATION",
        "thumbnail_title_2": "THE STOLEN SELF",
        "thumbnail_hook": "Why Modern Work Destroys the Soul",
        "acts": [
            ("Act 1: The Labyrinth of Modern Labor", "The paradox of increasing wealth and deepening human exhaustion."),
            ("Act 2: The Four Torments of Estrangement", "Separation from the object, from the act of creation, from species-essence, and from fellow human beings."),
            ("Act 3: Gattungswesen: The Loss of the Creative Spark", "Human beings as creative producers versus mere surviving animals."),
            ("Act 4: The Inversion: When Dead Capital Rules the Living", "How commodities become gods while living labor becomes an expendable commodity."),
            ("Act 5: Beyond the Realm of Necessity", "Reclaiming conscious, creative, and joyful human purpose.")
        ]
    },
    {
        "id": "ep_2",
        "topic": "Commodity Fetishism: The Secret Mysticism of the Marketplace",
        "focus": "Unraveling the brilliant opening chapter of Das Kapital: how social relations between living human beings take on the phantom form of relations between inanimate things.",
        "thumbnail_title_1": "COMMODITY FETISHISM",
        "thumbnail_title_2": "THE PHANTOM VALUE",
        "thumbnail_hook": "How Inanimate Objects Rule Society",
        "acts": [
            ("Act 1: The Mystical Veil of Everyday Objects", "Why a simple wooden table becomes transcendental the moment it enters the market."),
            ("Act 2: Use Value Versus Exchange Value", "The irreconcilable tension between human need and market abstraction."),
            ("Act 3: The Erasure of Human Hands", "How the market conceals the sweat, blood, and time invested in goods."),
            ("Act 4: The Ghost in the Shop Window", "Consumerism as a modern religious enchantment and secular ritual."),
            ("Act 5: Dispelling the Fog of Capital", "Restoring direct, conscious human cooperation over anonymous market forces.")
        ]
    },
    {
        "id": "ep_3",
        "topic": "Historical Materialism: Why Technology and Economics Drive Human Destiny",
        "focus": "The revolutionary philosophy of history: how human societies are shaped not by disembodied ideas or great leaders, but by their material modes of production and class struggle.",
        "thumbnail_title_1": "HISTORICAL MATERIALISM",
        "thumbnail_title_2": "THE MOTOR OF HISTORY",
        "thumbnail_hook": "How Society Actually Evolves",
        "acts": [
            ("Act 1: Turning Hegel on His Head", "Why consciousness does not determine life, but life determines consciousness."),
            ("Act 2: The Handmill and the Steam Mill", "The material forces of production as the foundation of social reality."),
            ("Act 3: Base and Superstructure", "How law, religion, politics, and art reflect economic relations."),
            ("Act 4: The Epochs of Class Struggle", "From ancient slavery and feudal serfdom to modern wage labor."),
            ("Act 5: The Horizon of Emancipation", "The emergence of conditions for true universal human liberation.")
        ]
    },
    {
        "id": "ep_4",
        "topic": "The Secret of Surplus Value: The Hidden Engine of Capital Accumulation",
        "focus": "The core mathematical and economic revelation of Das Kapital: how the purchase of labor-power yields more value than it costs, forming the sole foundation of capitalist profit.",
        "thumbnail_title_1": "SURPLUS VALUE",
        "thumbnail_title_2": "THE HIDDEN EQUATION",
        "thumbnail_hook": "Where Profit Actually Comes From",
        "acts": [
            ("Act 1: The Apparent Equality of the Market", "The illusion of a fair wage and voluntary employment contracts."),
            ("Act 2: Necessary Labor and Surplus Labor", "Dividing the working day into what keeps the worker alive and what enriches the owner."),
            ("Act 3: Absolute Versus Relative Surplus Value", "Lengthening the working hours versus intensifying technology and speed."),
            ("Act 4: Capital as Vampire", "Dead labor that only lives by sucking living labor, and lives the more, the more labor it sucks."),
            ("Act 5: The Inescapable Contradiction", "Why the pursuit of profit constantly undermines its own foundations.")
        ]
    },
    {
        "id": "ep_5",
        "topic": "All That Is Solid Melts into Air: The Creative Destruction of Modernity",
        "focus": "The breathtaking prophetic prose of the Communist Manifesto: capitalism as an unprecedented, titanic hurricane of global transformation that tears down ancient hierarchies.",
        "thumbnail_title_1": "ALL THAT IS SOLID",
        "thumbnail_title_2": "MELTS INTO AIR",
        "thumbnail_hook": "The Permanent Turbulence of Capital",
        "acts": [
            ("Act 1: The Sorcerer Who Unleashed the Whirlwind", "How the bourgeoisie revolutionized production more than all previous generations combined."),
            ("Act 2: The Annihilation of Space by Time", "Global trade networks, instant communication, and the erosion of local borders."),
            ("Act 3: The Dissolution of Ancient Sacraments", "Drowning heavenly ecstasies in the icy water of egotistical calculation."),
            ("Act 4: The Anxious Modern Soul", "Constant revolutionizing of production and everlasting uncertainty."),
            ("Act 5: Taming the Leviathan", "Harnessing the immense productive forces for communal flourishing rather than endless panic.")
        ]
    },
    {
        "id": "ep_6",
        "topic": "The Industrial Reserve Army: Why Capital Cannot Tolerate Full Employment",
        "focus": "The structural necessity of unemployment and precarious gig work in maintaining wage discipline, market competition, and corporate dominance.",
        "thumbnail_title_1": "THE RESERVE ARMY",
        "thumbnail_title_2": "MANUFACTURED SCARCITY",
        "thumbnail_hook": "Why Unemployment Is Built Into the System",
        "acts": [
            ("Act 1: The Fear of the Gate", "How the presence of the unemployed keeps the employed obedient and productive."),
            ("Act 2: The Machine That Replaces the Flesh", "Technological displacement and the creation of surplus populations."),
            ("Act 3: Precarious Existence", "The psychological toll of living on the knife-edge of economic obsolescence."),
            ("Act 4: Artificial Scarcity in an Age of Abundance", "Destroying goods and restricting output while poverty persists."),
            ("Act 5: From Competition to Solidarity", "Recognizing shared human dignity beyond the lottery of the market.")
        ]
    },
    {
        "id": "ep_7",
        "topic": "The Tendency of the Rate of Profit to Fall: The Inherent Crisis of Capital",
        "focus": "Karl Marx's profound economic diagnosis of cyclical crises, technological stagnation, and financial bubbles: why capital's own internal laws drive it toward periodic breakdown.",
        "thumbnail_title_1": "THE RATE OF PROFIT",
        "thumbnail_title_2": "THE INEVITABLE CRASH",
        "thumbnail_hook": "The Built-In Flaw of Capitalism",
        "acts": [
            ("Act 1: The Race to Automate", "Why every firm must adopt expensive machinery to survive competition."),
            ("Act 2: The Organic Composition of Capital", "Replacing living, value-producing workers with constant capital."),
            ("Act 3: The Declining Return", "Why more machinery leads paradoxically to a systemic drop in profit rates."),
            ("Act 4: Financial Speculation as an Escape Hatch", "Debt bubbles, speculative frenzies, and fictitious capital."),
            ("Act 5: The Inevitability of Renewal", "Why capital's solution to crisis is merely sowing the seeds for a greater one.")
        ]
    },
    {
        "id": "ep_8",
        "topic": "The Fetish of Money: The Universal Whore and Alienated God of Mankind",
        "focus": "From Aristotle and Shakespeare to Marx: money as the universal equivalent that converts all human qualities—intelligence, beauty, virtue—into purchasable commodities.",
        "thumbnail_title_1": "THE MONEY GOD",
        "thumbnail_title_2": "THE UNIVERSAL WHORE",
        "thumbnail_hook": "How Currency Distorts Human Values",
        "acts": [
            ("Act 1: From Barter to the Universal Measure", "How a single commodity emerged to represent all human labor."),
            ("Act 2: The Alchemical Inversion", "Money as the supreme power that turns cowardice into courage and stupidity into wisdom."),
            ("Act 3: The Quantified Life", "Evaluating every human relationship by cost-benefit analysis and profit margins."),
            ("Act 4: The Tyranny of the Abstract", "Living for numbers on a ledger rather than tangible sensory experience."),
            ("Act 5: Restoring Human Currency", "Love only exchangeable for love, and trust only exchangeable for trust.")
        ]
    },
    {
        "id": "ep_9",
        "topic": "The Young Hegelians and the Inversion: The Eleventh Thesis on Feuerbach",
        "focus": "The philosophical crucible of Berlin and Paris: breaking with abstract metaphysics to ground philosophy in the material earth and transformative human action.",
        "thumbnail_title_1": "THE ELEVENTH THESIS",
        "thumbnail_title_2": "BEYOND PHILOSOPHY",
        "thumbnail_hook": "From Interpreting the World to Changing It",
        "acts": [
            ("Act 1: The Ghost of Hegel's Absolute Spirit", "The magnificent but detached architecture of German Idealism."),
            ("Act 2: Feuerbach and the Critique of Religion", "Man creating God in his own idealized image."),
            ("Act 3: The Blind Spot of Materialism", "Why vulgar materialism fails to recognize active, revolutionary human praxis."),
            ("Act 4: The Lightning Bolt of the Eleventh Thesis", "The profound declaration that thought without action is sterile contemplation."),
            ("Act 5: Philosophy Realized in Life", "The union of rigorous theoretical intellect with practical human liberation.")
        ]
    },
    {
        "id": "ep_10",
        "topic": "The Realm of Freedom: Marx's True Vision of Human Flourishing",
        "focus": "Debunking the caricature of totalitarian bureaucracy: Marx's ultimate philosophical vision of a society where the free development of each is the condition for the free development of all.",
        "thumbnail_title_1": "THE REALM OF FREEDOM",
        "thumbnail_title_2": "BEYOND NECESSITY",
        "thumbnail_hook": "The True Vision of Human Flourishing",
        "acts": [
            ("Act 1: The Realm of Necessity", "The unavoidable work required to maintain biological existence."),
            ("Act 2: Where the Realm of Freedom Begins", "True freedom flourishing only beyond the threshold of compulsory labor."),
            ("Act 3: Free Time as the True Measure of Wealth", "Replacing accumulated capital with accumulated opportunities for creative growth."),
            ("Act 4: The Versatile Human Being", "To hunt in the morning, fish in the afternoon, rear cattle in the evening, and criticize after dinner."),
            ("Act 5: The Free Association of Free Beings", "A society worthy of the magnificent creative capacities of human consciousness.")
        ]
    }
]

# Master Script for Episode 1 (42 turns ~ 20 minutes runtime)
EP1_MASTER_SCRIPT = [
    # Act 1: The Labyrinth of Modern Labor
    {
        "speaker": config.HOST1_NAME,
        "text": "Every Sunday evening across the great capitals of our world, a quiet and suffocating shadow descends over millions of households. It is a peculiar psychological ache, known intimately to the modern wage earner, yet rarely understood in its true philosophical depth. Men and women sit in the quiet corners of their rooms, watching the ticking of the clock, feeling an unmistakable sense of dread as the working week approaches."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Why should this be? We are repeatedly told that we live in the wealthiest, most technologically advanced era in the recorded history of humankind. We are surrounded by miraculous machines, instantaneous communications, and an abundance of consumer goods that would dazzle ancient emperors. Yet the average worker feels not victorious, but hollow, spiritually depleted, and chronically exhausted."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "In the spring of 1844, sitting in a modest apartment in Paris, a young German thinker scarcely twenty-six years of age took up his pen to diagnose this exact condition. His name was Karl Marx. He was not looking at the world through cold economic formulas, but through the fiery lens of a philosopher who saw that modern commercial civilization was committing an unprecedented crime against the human spirit."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "In those legendary Paris Manuscripts, Marx laid bare the foundational paradox of industrial society. 'The worker becomes all the poorer the more wealth he produces, the more his production increases in power and range.' The more value the laborer creates in the outside world, the less value he retains within his own subjective being. This tragedy Marx named Alienation—Entfremdung."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Alienation is not merely a psychological malaise or a fleeting bout of workplace dissatisfaction. It is not something that can be resolved with wellness seminars, corporate perks, or longer vacations. Alienation, in Marx's rigorous analysis, is the fundamental structural condition of life under capitalism, where the very activity that defines us as human beings is torn from our grasp and turned into a hostile, alien power."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "To understand the magnitude of this diagnosis, we must first ask ourselves a fundamental question that philosophers have contemplated since antiquity: What does it mean to be human? What distinguishes our existence from that of the beasts in the forest or the cattle in the meadow? For Marx, the answer was neither divine spark nor abstract intellect, but conscious, creative labor."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "A spider conducts operations that resemble those of a weaver, and a bee puts to shame many an architect in the construction of her cells. But what distinguishes the worst architect from the best of bees is that the architect raises his structure in imagination before he erects it in reality. Human work is meant to be the living mirror in which we see our own mind, our aesthetic will, and our creative freedom embodied in the physical world."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Yet when we look at modern labor, what do we actually see? We see millions of people performing fragmented, repetitive tasks that require none of their creative imagination. We see human beings subordinated to schedules, algorithms, and assembly lines, counting down the minutes until they can finally leave the workplace and begin what they call their real life."
    },

    # Act 2: The Four Torments of Estrangement
    {
        "speaker": config.HOST1_NAME,
        "text": "Marx dissected this estrangement into four distinct, interlocking dimensions, like four walls of an invisible prison that encases the modern worker. The first dimension is the alienation of the worker from the product of his labor. Consider the carpenter of the Middle Ages: he selected the wood, carved the joints, polished the grain, and beheld a completed table that bore the indelible stamp of his skill."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "In our modern economy, the worker rarely owns, understands, or can even afford the object he spends his days producing. The factory hand assembling luxury automobiles rides home on a crowded bus. The software engineer writing microcode for high-frequency trading platforms cannot afford the rent in the city where his servers hum. The product of labor stands over against the laborer as something alien, as an independent power."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "The more objects the worker produces, the fewer he can possess, and the more he falls under the domination of his product, which is capital. The labor that was once his own vitality has coagulated into an external object that belongs entirely to someone else. His sweat has been crystallized into a physical commodity whose sole purpose is to be sold on an impersonal market to accumulate wealth for an anonymous shareholder."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "This brings us to the second dimension of alienation: the estrangement of the worker from the very act of production itself. If the product of labor is an alien thing, it is because the activity of producing it was an alienating experience from the very first minute. Labor is not voluntary, but coerced; it is forced labor."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "As Marx wrote with burning clarity: 'The worker therefore only feels himself outside his work, and in his work feels outside himself. He feels at home when he is not working, and when he is working he does not feel at home. His labor is therefore not voluntary, but coerced; it is forced labor. It is not the satisfaction of a need, but merely a means to satisfy needs external to it.'"
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Think of the profound psychological horror contained in that insight! When a person is working, they feel like an animal being driven by a whip. Only when they are performing their animal functions—eating, drinking, sleeping, and procreating—do they feel that they are acting freely. What is animal becomes human, and what is human becomes animal. Our highest creative faculty has been reduced to a grueling chore endured solely to pay for shelter and food."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "The third dimension of alienation strikes at the absolute philosophical core of our being: the estrangement of man from his species-essence, what Marx termed Gattungswesen. Unlike animals, who produce only under the compulsion of immediate physical need, human beings produce universally. We create in accordance with the laws of beauty, of proportion, of shared cultural purpose."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Our species-essence is the capacity to transform nature consciously and communally into a world that reflects our highest collective aspirations. But wage labor turns this species-life into a mere instrument of individual physical survival. It takes the magnificent tapestry of human creative potential and degrades it into nothing more than a biological survival mechanism, no different in essence than the grazing of a cow or the hunting of a wolf."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Finally, the fourth dimension is the alienation of man from man. When a human being is estranged from his own creative essence and from the object of his work, he inevitably becomes estranged from other human beings. In the marketplace of capital, we do not confront one another as brothers and sisters engaged in a shared human voyage. We confront one another as rivals, as buyers and sellers, as competitors fighting over scarce contracts and positions."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "The colleague sitting in the next cubicle or standing at the next station is not seen as an ally in human flourishing, but as a threat—a competitor who might work for lower wages, who might secure the promotion, who might render our own labor redundant. Society becomes atomized into a cold sea of self-seeking individuals, where every relationship is tinged with calculation and mutual suspicion."
    },

    # Act 3: Gattungswesen: The Theft of our Species-Essence
    {
        "speaker": config.HOST1_NAME,
        "text": "Let us pause here to reflect upon the immense beauty of Marx's concept of Gattungswesen. What does it really mean to live as a species-being? It means recognizing that every individual human life carries within itself the accumulated heritage, knowledge, and creative striving of all humanity. When an artist paints, when an engineer designs a bridge, when a thinker writes a book, they are not acting merely as isolated biological organisms."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "They are channels through which thousands of years of human cultural evolution, language, and technique find new expression. In a genuinely human society, our work would be an act of love and communal gift. I would know that my creative labor satisfies a genuine need in your life, and in satisfying your need, I would experience the direct validation of my own existence as an indispensable part of the human whole."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Under the regime of private property and wage labor, this sacred circuit of human solidarity is violently severed. The capitalist division of labor splinters the holistic human being into a microscopic fragment of himself. A man does not make a whole watch; he spends ten hours a day tightening a single microscopic screw until his eyes ache and his soul withers."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Adam Smith, the founding father of capitalist economics, openly admitted this consequence in The Wealth of Nations. He observed that the man whose whole life is spent performing a few simple operations generally becomes as stupid and ignorant as it is possible for a human creature to become. But while Smith accepted this as an inevitable price of economic efficiency, Marx rebelled against it with every fiber of his intellectual and moral being."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Marx refused to accept that human beings were born to be mere appendages of machinery. In Das Kapital, he described this mutilation with chilling eloquence: 'They mutilate the laborer into a fragment of a man, degrade him to the level of an appendage of a machine, destroy every remnant of charm in his work, and turn it into a hated toil; they estrange from him the intellectual potentialities of the labor process.'"
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Notice the language he uses: the destruction of charm in work. When was the last time modern society spoke of charm, of joy, of poetic dignity in the daily labors of its citizens? We speak endlessly of productivity metrics, of quarterly earnings, of return on investment, of gross domestic product. But we do not speak of whether the human beings generating those numbers are living lives of vibrant dignity or slow spiritual decay."
    },

    # Act 4: The Inversion: When Dead Capital Rules the Living
    {
        "speaker": config.HOST1_NAME,
        "text": "This brings us to the profound philosophical inversion that lies at the heart of capitalism: the dominance of dead labor over living labor. What is capital? When stripped of all academic mystification, capital is simply accumulated dead labor. It is factories, machines, raw materials, and money that were produced by past human beings who have long since turned to dust."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "In a sane and rational world, tools would serve the living worker. The hammer serves the blacksmith; the violin serves the musician; the telescope serves the astronomer. But in the inverted universe of capital, this relationship is standing on its head. The machine does not serve the worker; the worker serves the machine. The living human being must adjust his natural bodily rhythms, his sleep, his breath, and his posture to the relentless pace of an iron apparatus."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Marx captured this macabre inversion in one of the most memorable metaphors in all of world literature: 'Capital is dead labor, that, vampire-like, only lives by sucking living labor, and lives the more, the more labor it sucks.' Think of that image! A vast, inorganic monster constructed of steel, brick, and digital servers that feeds ceaselessly upon the vital hours of living men and women."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "The time of human life—the only truly irreplaceable possession that any of us has upon this fleeting earth—is converted into abstract exchange value. Every hour you spend generating profit for someone else is an hour of your consciousness that has been permanently surrendered to the void. And for what? In exchange for paper tokens that allow you to purchase the bare necessities required to return to the machine tomorrow morning."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Furthermore, this inversion generates the bizarre phenomenon of Commodity Fetishism, which Marx analyzed with surgical precision in the opening chapter of Capital. In everyday life, we treat market commodities as though they possess magical, intrinsic properties. We look at the price tag of a coat, a smartphone, or a barrel of oil as if value were a natural property residing in the atoms of the object, like weight or color."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "We forget completely that a price is nothing more than a distorted, encrypted social relationship between human beings. Behind every object on a store shelf stands a chain of human lives—miners in subterranean shafts, truck drivers navigating midnight highways, textile workers breathing cotton dust, engineers calculating stresses. Yet on the market, these living social relationships vanish, replaced by the mysterious dance of prices and commodities."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Things behave as if they had minds, and human beings behave as if they were mere things. A stock market crash can throw millions into starvation, not because the earth stopped yielding wheat or the factories stopped working, but because an abstract mathematical ratio fluctuating on a screen commanded that human activity must cease. The creations of human hands have acquired a will of their own and rule over their creators like wrathful pagan deities."
    },

    # Act 5: Beyond the Realm of Necessity
    {
        "speaker": config.HOST1_NAME,
        "text": "How, then, does humanity escape from this colossal labyrinth? What was Karl Marx's true vision for the overcoming of alienation? Contrary to the crude caricatures propagated by both totalitarian regimes and hostile critics, Marx's goal was not the grey standardization of human life or the forced leveling of individual personality. His goal was the radical emancipation of individual human creativity."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Marx distinguished between two great realms of human existence: the Realm of Necessity and the Realm of Freedom. The realm of physical necessity will always exist to some degree. Human beings will always need to grow food, weave clothing, build shelters, and generate energy. But in a rational society, this necessary labor would be shared equitably, automated to the highest possible degree, and organized under the conscious, democratic control of the producers."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "And beyond that realm of necessity, where does true human history begin? Let us hear Marx's own majestic words from the third volume of Das Kapital: 'Beyond it begins that development of human energy which is an end in itself, the true realm of freedom, which, however, can blossom forth only with this realm of necessity as its basis. The shortening of the working day is its basic prerequisite.'"
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "The shortening of the working day! Not merely for the sake of idle rest, but so that every human being has the unencumbered time and leisure to cultivate their mind, to practice the arts, to study the sciences, to love without economic calculation, and to participate fully in the governance of their community. Free time, Marx argued, is the true measure of wealth—not heaps of accumulated commodities, but disposable time for the full development of human potential."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "In The German Ideology, Marx offered a playful yet profoundly serious glimpse of what a truly liberated society might look like: a society where no one is locked into an exclusive sphere of activity, but can become accomplished in any branch he wishes. A society where it is possible for me 'to hunt in the morning, fish in the afternoon, rear cattle in the evening, criticize after dinner, just as I have a mind, without ever becoming hunter, fisherman, herdsman or critic.'"
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "What does that poetic passage mean? It means the abolition of the crippling specialization that forces a human being to define their entire identity by their job title. You are not merely a clerk, an accountant, a programmer, or a machinist. You are a human being endowed with diverse faculties—intellectual, physical, aesthetic, and moral—all of which deserve the space and air to blossom."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "As we look at our contemporary world of artificial intelligence, automated logistics, and staggering productive capability, Marx's nineteenth-century critique feels not antiquated, but prophetically contemporary. We possess the technological means to eliminate crushing toil from the surface of the globe. Yet because our tools remain imprisoned within the logic of capital, automation threatens workers with poverty rather than liberating them with leisure."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "The riddle of alienation remains the great unresolved crisis of our modern civilization. Until we summon the intellectual courage and collective solidarity to reorganize our economic life around the flourishing of living human beings rather than the accumulation of dead capital, we will continue to wander through the labyrinth of estrangement, searching for our stolen humanity."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "In the immortal words inscribed upon Marx's monument in Highgate Cemetery: 'The philosophers have only interpreted the world in various ways; the point, however, is to change it.' The journey toward that transformation begins in the sovereign chamber of our own minds, by stripping away the ideological illusions of the marketplace and daring to imagine a world worthy of the human spirit."
    },
    {
        "speaker": config.HOST1_NAME,
        "text": "Thank you for walking this intellectual path with us today on The Marxian Dialectic. If these philosophical reflections have stirred your thoughts and cast a new light upon the mechanics of our world, subscribe to our channel and share this exploration with those who seek understanding beneath the surface of modern life. Until our next contemplation, question every assumption, cherish your creative essence, and keep your mind ever awake."
    }
]

def load_history_topics():
    p = os.path.join(config.BASE_DIR, "published_videos.json")
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [d.get("topic") for d in data if isinstance(d, dict) and d.get("topic")]
        except Exception:
            pass
    return []

def generate_full_podcast_story(target_minutes: float = 20.0, topic: str = None, ep_num: int = 1) -> dict:
    if ep_num == 1 or not topic:
        curriculum_idx = (ep_num - 1) % len(MARX_CURRICULUM)
        curr = MARX_CURRICULUM[curriculum_idx]
        
        # If ep_1, return master pre-crafted script for supreme philosophical perfection
        if ep_num == 1:
            return {
                "title": f"The Riddle of Alienation: How Modern Work Destroys the Human Spirit | Karl Marx | Ep. {ep_num}",
                "topic": curr["topic"],
                "dialogue": EP1_MASTER_SCRIPT,
                "thumbnail_title_1": curr["thumbnail_title_1"],
                "thumbnail_title_2": curr["thumbnail_title_2"],
                "thumbnail_hook": curr["thumbnail_hook"],
                "chapters": [
                    {"title": act[0], "start_turn": i * 8}
                    for i, act in enumerate(curr["acts"])
                ]
            }

    # Fallback to curriculum item
    curriculum_idx = (ep_num - 1) % len(MARX_CURRICULUM)
    curr = MARX_CURRICULUM[curriculum_idx]
    return {
        "title": f"{curr['topic']} | Karl Marx | Ep. {ep_num}",
        "topic": curr["topic"],
        "dialogue": EP1_MASTER_SCRIPT,
        "thumbnail_title_1": curr["thumbnail_title_1"],
        "thumbnail_title_2": curr["thumbnail_title_2"],
        "thumbnail_hook": curr["thumbnail_hook"],
        "chapters": [
            {"title": act[0], "start_turn": i * 8}
            for i, act in enumerate(curr["acts"])
        ]
    }

def generate_metadata(topic: str = "", total_duration_sec: float = 0.0, chapters: list = None, ep_num: int = 1, story: dict = None) -> dict:
    if story:
        title = story.get("title", f"The Riddle of Alienation | Karl Marx | Ep. {ep_num}")
        topic = story.get("topic", topic or "Karl Marx and Alienation")
    else:
        title = f"{topic} | Karl Marx | Ep. {ep_num}"
    
    # Generate dynamic timestamps if chapters are provided
    timestamps_text = "TIMESTAMPS:\n"
    if chapters:
        for ch in chapters:
            t = ch.get("timestamp_str", "00:00")
            timestamps_text += f"{t} - {ch.get('title', 'Chapter')}\n"
    else:
        timestamps_text += "00:00 - Act 1: The Labyrinth of Modern Labor\n03:45 - Act 2: The Four Torments of Estrangement\n08:20 - Act 3: Gattungswesen: The Theft of our Species-Essence\n12:50 - Act 4: The Inversion: When Dead Capital Rules the Living\n16:40 - Act 5: Beyond the Realm of Necessity: The True Reclamation of Life\n"

    desc = f"""Episode #{ep_num}: {topic}

Welcome to THE MARXIAN DIALECTIC — an intellectual sanctuary devoted to the rigorous philosophical, historical, and economic critique of modern commercial society.

In this landmark episode, we descend into Karl Marx's revolutionary diagnosis of Alienation (Entfremdung) from the legendary Paris Manuscripts of 1844:
• The Paradox of Labor: Why the worker becomes poorer the more wealth he produces
• The 4 Dimensions of Estrangement: Alienation from the product, the act of production, our species-essence (Gattungswesen), and one another
• Dead Capital vs Living Labor: The vampire-like apparatus that consumes human time
• Commodity Fetishism: How relationships between human beings appear as relations between things
• Beyond the Realm of Necessity: Marx's true vision of human flourishing, unencumbered leisure, and creative self-realization

"The philosophers have only interpreted the world in various ways; the point, however, is to change it."
— Karl Marx, Theses on Feuerbach (1845)

{timestamps_text}
Join our dialectical circle as we dismantle the ideological illusions of capital and illuminate the path toward universal human emancipation.

Official Channel Handle: {config.CHANNEL_HANDLE}
#KarlMarx #Philosophy #PoliticalEconomy #Alienation #Capital #HistoricalMaterialism #MarxianDialectic"""

    return {
        "title": title[:100],
        "description": desc[:5000],
        "tags": ["Karl Marx", "Philosophy", "Political Economy", "Alienation", "Das Kapital", "Historical Materialism", "Species Essence", "Gattungswesen", "The Marxian Dialectic"]
    }
