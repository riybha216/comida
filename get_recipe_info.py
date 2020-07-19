import praw
import re
import argparse
import urllib.request

reddit = praw.Reddit(client_id='FsNxc6inwpcNcg',
                     client_secret='G5YggrO3hPrwy8IWvYvmOb8pzgA',
                     password='itchyspace13',
                     user_agent='get recipe info by /u/smiley_face435',
                     username='smiley_face435')
# keywords used in regex search to determine which comment contains the recipe
pattern = "(ingredient|cups|tsp|direction|recipe|instruction|milk|oil|serving|method|cost)"


class RecipeInfo:
    def __init__(self):
        self.top_listing = None

    # searching through posts in r/recipes to find one that is a recipe, matches the keyword, and has an image
    def init(self, recipe_keyword):
        print("\nTopic:", recipe_keyword)
        # sorting posts to find the one that includes the keyword and has the most upvotes
        listings = reddit.subreddit('recipes').search(recipe_keyword, sort='top')
        # searching through posts to find one that has an image and the 'Recipe' flair
        try:
            self.top_listing = next(x for x in listings if not x.is_self and x.link_flair_text == 'Recipe')
            print("\n{0}".format(self.top_listing.title))
        # end the search if there are no more matching posts remaining
        except StopIteration:
            print("No matching posts available for this search.")
            exit()

    # using a regex search to find the recipe in the post's comments
    def print_top_comment(self):
        prog = re.compile(pattern, re.MULTILINE)
        self.top_listing.comments.replace_more()
        match_in_post = prog.search(self.top_listing.selftext)
        # determining whether the common words found in recipes are in the post itself
        if match_in_post:
            print(self.top_listing.selftext)
        elif not match_in_post:
            # searching through the post's comments to find whether common recipe words exist in it
            for top_level_comment in self.top_listing.comments:
                match = prog.search(top_level_comment.body)
                if match and top_level_comment.is_submitter:
                    print(top_level_comment.body)

    # retrieving the image in the post and saving it as a local file
    def get_image(self, recipe_keyword):
        # renaming file to the appropriate name
        local_file_name = recipe_keyword + ".jpg"
        # retrieving the url of the image and saving it as a local file
        urllib.request.urlretrieve(self.top_listing.url, local_file_name)
        print("\nSaved local file: {0}".format(local_file_name))

    # pulling the username of the person who submitted the post
    def get_user_name(self):
        user_name = self.top_listing.author
        print("\nSource: u/{0}".format(user_name))


# main function
def main(args):
    r = RecipeInfo()
    r.init(args.recipe_keyword)
    r.print_top_comment()
    r.get_image(args.recipe_keyword)
    r.get_user_name()


if __name__ == "__main__":
    # creating an ArgumentParser object
    parser = argparse.ArgumentParser()
    parser.add_argument("recipe_keyword", help="Keyword to find recipes in the subreddit, r/recipes")
    main(parser.parse_args())
