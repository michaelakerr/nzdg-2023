import streamlit as st


def showAboutTheTour():
    st.header("About NZDG Tour Points System")
    st.markdown(
        """
        The NZDG Tour Points System is used to rank players who play in tournaments across New Zealand. 
        The system is is unique to suit the ever changing New Zealand disc golf scene.

        As per the growth of the sport, multiple scoring groups have been deemed necessary to implement and encourage both particiation in tour events,
        while also encouraging cross group competition for tournament directors (TD's).

        The scoring groups are:
        - Group 1: MPO
        - Group 2: MP40, MP50
        - Group 3: FPO, MA1
        - Group 4: MA40, MA50
        - Group 5: MA2
        - Group 6: ALL OTHER DIVISIONS - MA3, MA60, FA1, FA40, FA50, FA60, FA3, MA4, FA2, FA4, Junior Divisions etc

        Please find more information on scoring groups here: https://www.newzealanddiscgolf.org.nz/_files/ugd/acb9ce_d0f8c560ef694f55a30a420b4a9b6dd5.pdf

        ### How the Tour Points System allocates points
        - Tour Points are awarded to players based on their finishing position in their scoring group.
        - All scoring groups are elegibile for the total number of points at the tour event (for example 50 points in Group 1).
        - In the event of a tie for first in a division, a playoff should have occured, and PDGA will reflect this if the report is correctly updated.
        - However, this scoring system, does not take into account the playoff when there's multiple division in each scoring group as there is not a way to do this equitably

        ### Event Rankings
        - To calculate points, players are ranked by their finishing position in their scoring group.
        - Each score is evaluated by the number of players in the scoring group, and a rank is given. 
        ie the person with the lowest score across FPO and MA1 will be given a rank of 1, the second lowest is given a rank of 2 etc.  Ties are dealt with as per the previous section.

        ### Tour Points
        Points are allocated by the following formula:
        - event points per player = 1 + (tour points for the event-1) * (number of players in scoring group - players rank) / (number of players in scoring group - 1)

        ## Overall Tour Rankings
        - Tour Rankings are calculated by the sum of the best 6 tour events for each player, including at most 2 major events. The full policy is available here: https://www.newzealanddiscgolf.org.nz/_files/ugd/acb9ce_836d0cb72ab845be9073b1987bc5f49c.pdf
        - Major events are worth 70 points, and are indicated on the tour calendar as North Islands, South Islands, and National Championships.


        ## Tour feedback
        Players can give feedback on the tour by visiting this link:
        https://docs.google.com/forms/d/e/1FAIpQLSdeMRWGHI0wabvJAr8fga5WQIZRrQbTPWxL28SYHHdbFtSlxg/viewform

        ## Points system feedback
        Players can give feedback on the points system by emailing Michaela Kerr: mikki.mjk@gmail.com
        If you have points queries, please email me as well. 
        """
    )
    
showAboutTheTour()
